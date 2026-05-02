# ESTTA-Emulator

**Extremely Simple Transport Triggered Architecture**

ESTTA is an 8-bit Transport Triggered Architecture (TTA) CPU implementation consisting of a Python-based emulator and a custom assembler. Unlike traditional architectures (like x86 or ARM) that use a variety of opcodes for different operations, ESTTA operates using a single instruction: `move`. 

All computation, logic, and control flow are achieved as side effects of moving data into specialized hardware-mapped registers.

---

## Architecture Specification

The system operates on an 8-bit data bus with a 4-bit register address space. Each instruction is exactly 16 bits wide, representing a single transport from a source register to a destination register.

### Register Map

| Address | Symbol | Description |
| :--- | :--- | :--- |
| `0x0` | `CONSTANT_0` | Hardwired to 0. Writing here acts as a NOP. |
| `0x1` | `CONSTANT_1` | Hardwired to 1. |
| `0x2` | `DISPLAY1` | Virtual 4x4 LED Display (Rows 1-2). |
| `0x3` | `DISPLAY2` | Virtual 4x4 LED Display (Rows 3-4). |
| `0x4` | `PC` | Program Counter. Writing an address here triggers a jump. |
| `0x5` | `REG6` | General-purpose register. |
| `0x6` | `REG7` | General-purpose register. |
| `0x7` | `REG8` | General-purpose register. |
| `0x8` | `REG9` | General-purpose register. |
| `0x9` | `REG10` | General-purpose register. |
| `0xA` | `REG11` | General-purpose register. |
| `0xB` | `CONDITIONAL_OUT` | Destination register for conditional moves. |
| `0xC` | `CONDITIONAL_IN` | Source register for conditional moves. |
| `0xD` | `ALU_INPUT_A` | Subtractor operand A. |
| `0xE` | `ALU_INPUT_B` | Subtractor operand B. |
| `0xF` | `ALU_OUTPUT` | Result of `ALU_INPUT_A - ALU_INPUT_B`. |

### The ALU and Conditional Logic

The Arithmetic Logic Unit (ALU) is a dedicated subtractor. Because the CPU utilizes 8-bit wraparound (modulo 256), all standard arithmetic (addition, multiplication by 2, negation) is derived mathematically through subtraction.

Conditionals are handled via a hardware trigger. If the value in `ALU_OUTPUT` is exactly zero, the processor automatically performs an internal move: the value currently in `CONDITIONAL_IN` is copied to `CONDITIONAL_OUT`. 

To perform a conditional jump (e.g., "Branch if Equal"):
1. Load the jump target address into `CONDITIONAL_IN`.
2. Move the address of the `PC` register into `CONDITIONAL_OUT`.
3. Perform a subtraction. If the result is 0, the target address is moved to the `PC`, and the jump occurs.

---

## Toolchain Usage

### 1. Assembler (`assembler.py`)
The assembler translates `.asm` source files into 16-bit binary ROM files. It supports definitions, recursive file inclusion, and the `move` syntax.

**Syntax Examples:**
* `move <SRC> <DEST>`: Primary instruction.
* `define <HEX_VAL> <NAME>`: Creates a symbolic constant.
* `include %filename.asm%`: Inlines code from another file.

**Command:**
```bash
python assembler.py your_code.asm
