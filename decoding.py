# Branch instructions
def decode_SB(instruction):
    imm_cycle_32 = instruction[:7]
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    # offset do branch
    imm_offset = instruction[20:25]
    opcode = instruction[25:]

    return imm_cycle_32, rs2, rs1, funct3, imm_offset, opcode


# Load immediate logic instructions
def decode_I(instruction):
    # can be offset in load or constant in logic
    imm = instruction[:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    rd = instruction[20:25]
    opcode = instruction[25:]

    return imm, rs1, funct3, rd, opcode


# Storing the instructions
def decode_S(instruction):
    imm_cycle_32 = instruction[:7]
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    imm_offset = instruction[20:25]
    opcode = instruction[25:]

    return imm_cycle_32, rs2, rs1, funct3, imm_offset, opcode


# shift and non-immediate instructions
def decode_R(instruction):
    funct7 = instruction[:7]
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    rd = instruction[20:25]
    opcode = instruction[25:]

    return funct7, rs2, rs1, funct3, rd, opcode


# simply JAL
def decode_UJ(instruction):
    imm = instruction[:20]
    rd = instruction[20:25]


# HE and AUIPC
def decode_U(instruction):
    imm = instruction[:20]
    rd = instruction[20:25]