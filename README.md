# RISC-V Single Stage Core Interpreter

This project implements a 32-bit RISC-V single-stage core interpreter. It simulates the execution of RISC-V instructions using an instruction memory, data memory, and register file. The program processes multiple test cases, executes instructions, and outputs the results, including performance metrics.

---

## Features

- **Instruction Memory**: Reads and decodes RISC-V instructions from `imem.txt`.
- **Data Memory**: Reads and writes data to `dmem.txt` during instruction execution.
- **Register File**: Simulates 32 general-purpose registers for the RISC-V architecture.
- **Instruction Types Supported**:
  - R-Type: `ADD`, `SUB`, `XOR`, `OR`, `AND`
  - I-Type: `ADDI`, `XORI`, `ORI`, `ANDI`, `LW`
  - S-Type: `SW`
  - SB-Type: `BEQ`, `BNE`
  - UJ-Type: `JAL`
  - HALT
- **Performance Metrics**: Calculates and outputs:
  - Number of instructions executed
  - Number of cycles taken
  - Cycles per instruction (CPI)
  - Instructions per cycle (IPC)

---

## File Structure
```
Bin2ASM-RV/ 

├── code/

│ ├── input/ 

│ │ ├── testcase0/ 

│ │ │ ├── imem.txt 

│ │ │ ├── dmem.txt 

│ │ ├── testcase1/ 

│ │ │ ├── imem.txt 

│ │ │ ├── dmem.txt 

│ │ ├── testcase2/ 

│ │ ├──├── imem.txt 

│ │ ├──├── dmem.txt 

│ ├── main.py 

├── README.md
```
---

## How to Run

### Prerequisites
- Python 3.6 or higher
- No external dependencies are required.

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Bin2ASM-RV
   ```
2. Run the program:
   ```bash
   python3 main.py --iodir /{project-directory}/input/
   ```
3. The program will process all test cases (testcase0, testcase1, testcase2) and generate output files in their respective directories.

## Output Files
For each test case, the following output files are generated:

1. StateResult_SS.txt: State of the core after each cycle.
   
2. RFResult.txt: Final state of the register file.
   
3. SS_DMEMResult.txt: Final state of the data memory.

4. PerformanceMetrics_Result.txt: Performance metrics for the test case.
