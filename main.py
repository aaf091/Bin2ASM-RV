import os
import argparse

MEMORY_SIZE = 1000  # Limited for the lab; memory remains 32-bit addressable

class InstructionMemory:
    def __init__(self, name, io_dir):
        self.name = name
        self.io_dir = io_dir
        with open(os.path.join(io_dir, "imem.txt")) as file:
            self.memory = [line.strip() for line in file]

    def read_instruction(self, address):
        addr = int(address)
        # Use slicing to get 4 bytes and then join them
        instruction_bits = ''.join(self.memory[addr:addr + 4])
        return hex(int(instruction_bits, 2))

    def decode_instruction(self, instruction_hex):
        binary_inst = bin(int(instruction_hex, 16))[2:].zfill(32)
        # Slice out parts of the binary instruction
        opcode      = binary_inst[-7:]
        r_field     = binary_inst[-12:-7]
        funct3      = binary_inst[-15:-12]
        rs1_bits    = binary_inst[-20:-15]
        rs2_bits    = binary_inst[-25:-20]
        funct7      = binary_inst[-32:-25]

        args = {}
        command = ""

        # HALT Instruction
        if opcode == '1111111':
            args['type'] = 'HALT'
            args['method'] = 'HALT'
            command = "HALT"

        # R-Type Instructions
        elif opcode == "0110011":
            args['type'] = 'R'
            args['rd'] = int(r_field, 2)
            args['funct3'] = funct3
            args['rs1'] = int(rs1_bits, 2)
            args['rs2'] = int(rs2_bits, 2)
            args['funct7'] = funct7

            if funct3 == '000' and funct7 == '0000000':
                method = 'ADD'
            elif funct3 == '000' and funct7 == '0100000':
                method = 'SUB'
            elif funct3 == '100' and funct7 == '0000000':
                method = 'XOR'
            elif funct3 == '110' and funct7 == '0000000':
                method = 'OR'
            elif funct3 == '111' and funct7 == '0000000':
                method = 'AND'
            args['method'] = method
            command = f"{method} x{args['rd']}, x{args['rs1']}, x{args['rs2']}"

        # I-Type Instructions
        elif opcode in ["0010011", "0000011"]:
            args['type'] = 'I'
            args['rd'] = int(r_field, 2)
            args['funct3'] = funct3
            args['rs1'] = int(rs1_bits, 2)
            # Immediate is concatenated from funct7 and rs2_bits
            imm_bits = funct7 + rs2_bits
            # Sign extension for the immediate value
            if imm_bits[0] == '1':
                imm = -((int(''.join('1' if c == '0' else '0' for c in imm_bits), 2)) + 1)
            else:
                imm = int(imm_bits, 2)
            args['imm'] = imm
            args['imm_raw'] = int(imm_bits, 2)

            if opcode == '0010011':
                if funct3 == '000':
                    method = 'ADDI'
                elif funct3 == '100':
                    method = 'XORI'
                elif funct3 == '110':
                    method = 'ORI'
                elif funct3 == '111':
                    method = 'ANDI'
                args['method'] = method
                command = f"{method} x{args['rd']}, x{args['rs1']}, {imm}"
            elif opcode == '0000011':
                if funct3 == '000':
                    method = 'LW'
                args['method'] = method
                command = f"{method} x{args['rd']}, {imm}(x{args['rs1']})"

        # S-Type Instructions
        elif opcode == "0100011":
            args['type'] = 'S'
            args['funct3'] = funct3
            args['rs1'] = int(rs1_bits, 2)
            args['rs2'] = int(rs2_bits, 2)
            imm_low = r_field
            imm_high = funct7
            imm_str = imm_high + imm_low
            if imm_str[0] == '1':
                imm = -((int(''.join('1' if c == '0' else '0' for c in imm_str), 2)) + 1)
            else:
                imm = int(imm_str, 2)
            args['imm'] = imm
            args['imm_low'] = int(imm_low, 2)
            args['imm_high'] = int(imm_high, 2)
            method = 'SW'  # Only SW is defined
            args['method'] = method
            command = f"{method} x{args['rs2']}, {imm}(x{args['rs1']})"

        # SB-Type Instructions
        elif opcode == "1100011":
            args['type'] = 'SB'
            args['funct3'] = funct3
            args['rs1'] = int(rs1_bits, 2)
            args['rs2'] = int(rs2_bits, 2)
            # Reconstruct immediate from parts of the binary instruction
            imm_str = "".join((binary_inst[0], binary_inst[-8], binary_inst[-31:-25], binary_inst[-12:-8], "0"))
            if imm_str[0] == "0":
                imm = int(imm_str, 2)
            else:
                imm = -((~int(imm_str, 2) & 0b11111111111) + 1)
            args['imm'] = imm

            if funct3 == '000':
                method = 'BEQ'
            elif funct3 == '001':
                method = 'BNE'
            args['method'] = method
            command = f"{method} x{args['rs1']}, x{args['rs2']}, label #imm = {imm}"

        # UJ-Type Instructions
        elif opcode == "1101111":
            args['type'] = 'J'
            args['rd'] = int(r_field, 2)
            # Construct immediate using specific bit groupings
            imm_str = "".join((binary_inst[0], binary_inst[-20:-12], binary_inst[-21], binary_inst[-31:-21]))
            if imm_str[0] == "0":
                imm = int(imm_str, 2)
            else:
                imm = -((~int(imm_str, 2) & 0b11111111111) + 1)
            args['imm'] = imm
            args['method'] = 'JAL'
            command = f"JAL x{args['rd']}, {imm}"

        print(command)
        return args

class DataMemory:
    def __init__(self, name, io_dir):
        self.name = name
        self.io_dir = io_dir
        with open(os.path.join(io_dir, "dmem.txt")) as file:
            self.memory = [line.strip() for line in file]
        # Pad the memory to ensure it reaches the lab's limit
        self.memory += ["00000000"] * (MEMORY_SIZE - len(self.memory))

    def read_data(self, address, mode='word'):
        try:
            addr = int(address, 16)
        except Exception:
            addr = address
        if mode == 'word':
            data_str = ''.join(self.memory[addr:addr + 4])
        elif mode == 'half':
            data_str = ''.join(self.memory[addr + 2:addr + 4])
        elif mode == 'byte':
            data_str = self.memory[addr + 3]
        return int(data_str, 2)

    def write_data(self, address, value, mode='word'):
        try:
            addr = int(address, 16)
        except Exception:
            addr = address
        data_bin = format(value & 0xFFFFFFFF, '032b')
        # Split into bytes (8 bits each)
        byte_list = [data_bin[i:i + 8] for i in range(0, 32, 8)]
        if mode == 'word':
            start, end = 0, 4
        elif mode == 'half':
            start, end = 2, 4
        elif mode == 'byte':
            start, end = 3, 4
        for i in range(start, end):
            self.memory[addr + i] = byte_list[i]

    def dump_memory(self):
        result_path = os.path.join(self.io_dir, f"{self.name}_DMEMResult.txt")
        with open(result_path, "w") as file:
            file.writelines(data + "\n" for data in self.memory)

class RegisterFile:
    def __init__(self, io_dir):
        self.output_file = os.path.join(io_dir, "RFResult.txt")
        # Initialize 32 registers with 32-bit zeros
        self.registers = ["0b" + "0" * 32 for _ in range(32)]

    def read_register(self, reg_addr):
        value_bin = self.registers[reg_addr]
        value = int(value_bin, 2)
        # Adjust for negative numbers if the sign bit is set
        if value_bin[2] == '1':
            value -= 2**32
        return value

    def write_register(self, reg_addr, value):
        if reg_addr != 0:
            bin_value = bin(value & 0xFFFFFFFF)[2:].zfill(32)
            self.registers[reg_addr] = bin_value

    def dump_registers(self, cycle):
        header = "\nState of RF after executing cycle: " + str(cycle) + "\n"
        regs = [reg.replace("0b", "") + "\n" for reg in self.registers]
        mode = "w" if cycle == 0 else "a"
        with open(self.output_file, mode) as file:
            file.write("\n" + header)
            file.writelines(regs)

class CoreState:
    def __init__(self):
        self.IF = {"nop": False, "PC": 0}
        self.ID = {"nop": True, "Instr": 0, "is_hazard": False}
        self.EX = {"nop": True, "Read_data1": 0, "Read_data2": 0, "Imm": 0, "Rs": 0, "Rt": 0, 
                   "Wrt_reg_addr": 0, "is_I_type": False, "rd_mem": 0, "wrt_mem": 0, 
                   "alu_op": 0, "wrt_enable": 0}
        self.MEM = {"nop": True, "ALUresult": 0, "Store_data": 0, "Rs": 0, "Rt": 0, 
                    "Wrt_reg_addr": 0, "rd_mem": 0, "wrt_mem": 0, "wrt_enable": 0}
        self.WB = {"nop": True, "Wrt_data": 0, "Rs": 0, "Rt": 0, "Wrt_reg_addr": 0, "wrt_enable": 0}

class BaseCore:
    def __init__(self, io_dir, instr_mem, data_mem):
        self.rf = RegisterFile(io_dir)
        self.cycle = 0
        self.halted = False
        self.io_dir = io_dir
        self.state = CoreState()
        self.next_state = CoreState()
        self.instr_mem = instr_mem
        self.data_mem = data_mem

class SingleStageCore(BaseCore):
    def __init__(self, io_dir, instr_mem, data_mem):
        super().__init__(os.path.join(io_dir, "SS_"), instr_mem, data_mem)
        self.state_result_file = os.path.join(io_dir, "StateResult_SS.txt")
        self.halted = False

    def step(self):
        if self.state.IF["nop"]:
            self.halted = True
        else:
            self.next_state.IF["nop"] = False
            self.next_state.IF["PC"] = self.state.IF["PC"]

            inst_hex = self.instr_mem.read_instruction(self.next_state.IF["PC"])
            args = self.instr_mem.decode_instruction(inst_hex)

            # R-Type Instructions
            if args['type'] == 'R':
                reg1 = self.rf.read_register(args['rs1'])
                reg2 = self.rf.read_register(args['rs2'])
                if args['method'] == 'ADD':
                    result = reg1 + reg2
                elif args['method'] == 'SUB':
                    result = reg1 - reg2
                elif args['method'] == 'XOR':
                    result = reg1 ^ reg2
                elif args['method'] == 'OR':
                    result = reg1 | reg2
                elif args['method'] == 'AND':
                    result = reg1 & reg2
                self.rf.write_register(args['rd'], result)
                self.next_state.IF["PC"] += 4

            # I-Type Instructions
            elif args['type'] == 'I':
                reg1 = self.rf.read_register(args['rs1'])
                imm = args['imm']
                if args['method'] == 'ADDI':
                    result = reg1 + imm
                elif args['method'] == 'XORI':
                    result = reg1 ^ imm
                elif args['method'] == 'ORI':
                    result = reg1 | imm
                elif args['method'] == 'ANDI':
                    result = reg1 & imm
                elif args['method'] == 'LW':
                    result = self.data_mem.read_data(hex(reg1 + imm), mode='word')
                self.rf.write_register(args['rd'], result)
                self.next_state.IF["PC"] += 4

            # S-Type Instructions
            elif args['type'] == 'S':
                reg1 = self.rf.read_register(args['rs1'])
                reg2 = self.rf.read_register(args['rs2'])
                imm = args['imm']
                self.data_mem.write_data(hex(reg1 + imm), reg2, mode='word')
                self.next_state.IF["PC"] += 4

            # SB-Type Instructions
            elif args['type'] == 'SB':
                reg1 = self.rf.read_register(args['rs1'])
                reg2 = self.rf.read_register(args['rs2'])
                imm = args['imm']
                if args['method'] == 'BEQ':
                    self.next_state.IF["PC"] += imm if reg1 == reg2 else 4
                elif args['method'] == 'BNE':
                    self.next_state.IF["PC"] += imm if reg1 != reg2 else 4

            # JAL Instruction
            elif args.get('method') == 'JAL':
                imm = args['imm']
                self.rf.write_register(args['rd'], self.next_state.IF["PC"] + 4)
                self.next_state.IF["PC"] = self.next_state.IF["PC"] + imm * 2

            # HALT Instruction
            elif args['method'] == 'HALT':
                self.next_state.IF["nop"] = True

        self.rf.dump_registers(self.cycle)
        self._print_state(self.next_state, self.cycle)
        self.state = self.next_state
        self.cycle += 1

    def _print_state(self, state, cycle):
        lines = [
            "-" * 70 + "\n",
            "State after executing cycle: " + str(cycle) + "\n",
            "IF.PC: " + str(state.IF["PC"]) + "\n",
            "IF.nop: " + str(state.IF["nop"]) + "\n"
        ]
        mode = "w" if cycle == 0 else "a"
        with open(self.state_result_file, mode) as file:
            file.writelines(lines)

def print_performance_metrics(io_dir, instructions, cpi, ipc, cycles):
    output_path = os.path.join(io_dir, "PerformanceMetrics_Result.txt")
    lines = [
        "Single Stage Core Performance Metrics:\n",
        "Number of instructions: " + str(instructions) + "\n",
        "Number of cycles taken: " + str(cycles) + "\n",
        "Cycles per instruction: " + str(cpi) + "\n",
        "Instructions per cycle: " + str(ipc) + "\n\n\n"
    ]
    with open(output_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    path_list = ['testcase0', 'testcase1', 'testcase2']

    parser = argparse.ArgumentParser(description='32-bit RISC-V Interpreter')
    parser.add_argument('--iodir', default="/Users/aaditfadia/Downloads/CSA Project/Bin2ASM-RV/input/", type=str, help='Base directory containing input files.')
    args = parser.parse_args()

    base_io_directory = os.path.abspath(args.iodir)

    for path in path_list:
        curr_path = os.path.join(base_io_directory, path)
        print("IO Directory:", curr_path)

        instr_mem = InstructionMemory("Imem", curr_path)
        data_mem = DataMemory("SS", curr_path)
        core = SingleStageCore(curr_path, instr_mem, data_mem)

        # Execute the single stage core until halted
        while not core.halted:
            core.step()

        # Dump final data memory contents
        data_mem.dump_memory()

        total_cycles = core.cycle
        total_instructions = total_cycles - 1
        cpi = round(total_cycles / total_instructions, 6)
        ipc = round(1 / cpi, 6)
        print(f"\nCPI: {cpi}")
        print(f"\nIPC: {ipc}")

        print_performance_metrics(curr_path, total_instructions, cpi, ipc, total_cycles)