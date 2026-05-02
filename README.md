# ESTTA-Emulator

**Extremely Simple Transport Triggered Architecture**

ESTTA is an 8-bit Transport Triggered Architecture (TTA) CPU implementation featuring a Python-based emulator and a custom assembler. In this architecture, there is no traditional instruction set; the system operates using a single instruction: `move`. All computation and control flow are triggered as side effects of moving data into specialized registers.

## Architecture Overview

The system utilizes a 16-register address space (0x0 to 0xF) and 8-bit data width.

### Register Map

| Address | Symbol | Description |
| :--- | :--- | :--- |
| `0x0` | `CONSTANT_0` | Hardwired to 0. Writing here acts as a NOP. |
| `0x1` | `CONSTANT_1` | Hardwired to 1. |
| `0x2` | `DISPLAY1` | 4x4 LED Display (Rows 1-2). |
| `0x3` | `DISPLAY2` | 4x4 LED Display (Rows 3-4). |
| `0x4` | `PC` | Program Counter. Writing an address here triggers a jump. |
| `0x5` | `REG6` | General-purpose register. |
| `0x6` | `REG7` | General-purpose register. |
| `0x7` | `REG8` | General-purpose register. |
| `0x8` | `REG9` | General-purpose register. |
| `0x9` | `REG10` | General-purpose register. |
| `0xA` | `REG11` | General-purpose register. |
| `0xB` | `CONDITIONAL_OUT` | Conditional output destination. |
| `0xC` | `CONDITIONAL_IN` | Conditional input source. |
| `0xD` | `ALU_INPUT_A` | First operand for the subtractor. |
| `0xE` | `ALU_INPUT_B` | Second operand for the subtractor. |
| `0xF` | `ALU_OUTPUT` | Result of `ALU_INPUT_A - ALU_INPUT_B`. |

### Computation and Control Flow
The ALU is an 8-bit subtractor. To perform a calculation, move values into `ALU_INPUT_A` and `ALU_INPUT_B`, then read the result from `ALU_OUTPUT`.

Conditional logic is handled by a hardware trigger:
**If `ALU_OUTPUT` (0xF) is equal to 0, the CPU automatically copies the value in `CONDITIONAL_IN` (0xC) to `CONDITIONAL_OUT` (0xB).**

To perform a conditional jump, move the target address into `CONDITIONAL_IN` and set `CONDITIONAL_OUT` to the `PC` (0x4).

---

## Toolchain Usage

### 1. The Assembler (`assembler.py`)
The assembler processes `.asm` files into binary ROM files. It supports definitions, includes, and `move` operations.

**Syntax:**
* `move <source> <destination>`: Transports data between registers.
* `define <value> <symbol>`: Maps a value or address to a name.
* `include %file.asm%`: Includes an external assembly file.

**Command:**
```bash
python assembler.py main.asm