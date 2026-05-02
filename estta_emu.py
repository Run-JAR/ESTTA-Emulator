#!/usr/bin/env python3
"""
ESTTA TTA CPU Emulator - Minimal UI with 4x4 LED Display
Updated: 4x4 LED grid, simplified styling
"""

import sys, os, time, argparse, re

# Fix Windows encoding for UTF-8 characters
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── terminal colours (minimal palette) ─────────────────────────────────────────
ESC = "\033["
def fg(r,g,b):   return f"{ESC}38;2;{r};{g};{b}m"
def bg(r,g,b):   return f"{ESC}48;2;{r};{g};{b}m"
RST  = f"{ESC}0m"
BOLD = f"{ESC}1m"

C_GREEN   = fg(100,200,100)
C_DIM     = fg(80,80,80)
C_WHITE   = fg(200,200,200)
C_ACCENT  = fg(100,180,255)

HIDE_CURSOR = f"{ESC}?25l"
SHOW_CURSOR = f"{ESC}?25h"
CLEAR       = f"{ESC}2J{ESC}H"

# ── register metadata (from reg_names.asm) ──────────────────────────────────────
REG_NAMES = {
    0x0:  "CONST_0",     0x1:  "CONST_1",
    0x2:  "DISPLAY1",    0x3:  "DISPLAY2",
    0x4:  "PC",
    0x5:  "REG6",        0x6:  "REG7",        0x7:  "REG8",        0x8:  "REG9",
    0x9:  "REG10",       0xA:  "REG11",
    0xB:  "COND_OUT",
    0xC:  "COND_IN",
    0xD:  "ALU_A",
    0xE:  "ALU_B",
    0xF:  "ALU_OUT",
}
SPECIAL = {0x0, 0x1, 0x4, 0xD, 0xE, 0xF, 0xB, 0xC}

def render_led_grid(val1, val2):
    """Render a 4x4 LED grid from two 8-bit values."""
    bits = format(val1, '08b') + format(val2, '08b')
    grid = []
    for row in range(4):
        row_str = ""
        for col in range(4):
            bit_idx = row * 4 + col
            is_on = bits[bit_idx] == '1'
            row_str += f"{C_GREEN}■{RST} " if is_on else "◻ "
        grid.append(f"    {row_str}")
    return grid

# ── ROM parsing ───────────────────────────────────────────────────────────────
def parse_rom(path):
    instructions = []
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line: continue
            bits = line.replace(" ", "")
            if len(bits) != 16 or not all(c in '01' for c in bits): continue
            src = int(bits[8:12][::-1], 2)
            dst = int(bits[12:16], 2)
            instructions.append((src, dst))
    while len(instructions) < 256: instructions.append((0, 0))
    return instructions[:256]

def instr_byte(src, dst): return ((src & 0xF) << 4) | (dst & 0xF)

def disasm(src, dst):
    sn = REG_NAMES.get(src, f"R{src}")
    dn = REG_NAMES.get(dst, f"R{dst}")
    if src == 0 and dst == 0: 
        return "NOP"
    if dst == 0x4: 
        return f"JMP  {sn}"
    if dst == 0x0: 
        return f"NOP  ({sn}→CONST_0)"
    return f"MOVE {sn} → {dn}"

# ── CPU ───────────────────────────────────────────────────────────────────────
class ESTTA:
    def __init__(self, rom):
        self.rom = rom
        self.regs = [0] * 17
        self.pc = 0
        self.cycles = 0
        self.last_dst = -1
        self.last_src = -1
        self._update_alu()

    def _update_alu(self):
        # ALU: ALU_A (0xD) - ALU_B (0xE)
        a, b = self.regs[0xD], self.regs[0xE]
        result = (a - b) & 0xFF
        self.alu_out = result
        self.ifzero = (result == 0)
        self.regs[0xF] = result  # ALU_OUT

    def step(self):
        src, dst = self.rom[self.pc & 0xFF]
        self.last_src, self.last_dst = src, dst
        
        # Get source value
        if src == 0x0:
            val = 0  # CONST_0
        elif src == 0x1:
            val = 1  # CONST_1
        elif src == 0x4:
            val = self.pc  # PC
        else:
            val = self.regs[src]
        
        # Write to destination
        if dst == 0x4:
            # Writing to PC updates it directly
            self.pc = val & 0xFF
        elif dst != 0x0:  # Don't write to CONST_0
            self.regs[dst] = val & 0xFF
        
        self._update_alu()
        # Always increment PC (even when we just wrote to it)
        self.pc = (self.pc + 1) & 0xFF
        self.cycles += 1

    def reg_val(self, r):
        if r == 0x0:
            return 0
        elif r == 0x1:
            return 1
        elif r == 0x4:
            return self.pc
        else:
            return self.regs[r]

# ── UI rendering ──────────────────────────────────────────────────────────────
def render(cpu, rom_instructions, step_mode, hz_val):
    lines = []
    def strip_ansi(s): return re.sub(r'\033\[[^m]*m', '', s)

    # Header
    title = f"{C_GREEN}ESTTA TTA CPU Emulator{RST}"
    mode  = f"{C_DIM}[{'STEP' if step_mode else 'RUN'}]{RST}"
    lines.append(f"{title}   {mode}")
    lines.append(f"{C_DIM}{'─'*70}{RST}")

    # Registers (all 16)
    lines.append(f"{C_GREEN}REGISTERS{RST}")
    for r in range(0, 16):
        v = cpu.reg_val(r)
        name = REG_NAMES[r]
        is_written = r == cpu.last_dst
        is_special = r in SPECIAL
        
        status = ""
        if is_written:
            status = f" {C_ACCENT}[WRITTEN]{RST}"
        elif is_special:
            status = f" {C_DIM}[special]{RST}"
        
        lines.append(f"  {C_WHITE}{name:<9}{RST} = 0x{v:02X}  ({v:>3}){status}")

    lines.append(f"{C_DIM}{'─'*70}{RST}")

    # Instruction & ALU
    src, dst = cpu.rom[cpu.pc & 0xFF]
    byte = instr_byte(src, dst)
    
    lines.append(f"{C_GREEN}INSTRUCTION{RST}  0x{byte:02X}  ({disasm(src,dst)})")
    lines.append(f"  SRC: {src:X}  DST: {dst:X}")
    lines.append(f"{C_DIM}{'─'*70}{RST}")

    lines.append(f"{C_GREEN}ALU (ALU_A - ALU_B){RST}")
    lines.append(f"  A={cpu.regs[0xD]:3d}  B={cpu.regs[0xE]:3d}  OUT={cpu.alu_out:3d}  IFZ={int(cpu.ifzero)}")
    lines.append(f"{C_DIM}{'─'*70}{RST}")

    # Display Grid
    lines.append(f"{C_GREEN}LED DISPLAY (4×4)  [DISPLAY1:DISPLAY2]{RST}")
    led_grid = render_led_grid(cpu.regs[0x2], cpu.regs[0x3])
    for row in led_grid:
        lines.append(row)
    lines.append(f"  DISPLAY1=0x{cpu.regs[0x2]:02X}  DISPLAY2=0x{cpu.regs[0x3]:02X}")
    lines.append(f"{C_DIM}{'─'*70}{RST}")

    # PC & Status
    lines.append(f"{C_GREEN}STATUS{RST}")
    lines.append(f"  PC={cpu.pc:3d} (0x{cpu.pc:02X})   CYCLES={cpu.cycles}")
    lines.append(f"{C_DIM}{'─'*70}{RST}")

    # ROM window
    lines.append(f"{C_GREEN}ROM{RST}  (◄ = current PC)")
    pc = cpu.pc & 0xFF
    win_start = max(0, min(246, pc - 3))
    for i in range(win_start, min(win_start + 8, 256)):
        rs, rd = rom_instructions[i]
        is_current = (i == pc)
        marker = f"{C_ACCENT}◄{RST} " if is_current else "  "
        instr = disasm(rs, rd)
        byte = instr_byte(rs, rd)
        prefix = f"{C_ACCENT}" if is_current else f"{C_WHITE}"
        lines.append(f"  {marker}{prefix}{i:02X}{RST} 0x{byte:02X}  {instr}")

    lines.append(f"{C_DIM}{'─'*70}{RST}")
    if step_mode:
        lines.append(f"{C_GREEN}[ENTER]{RST} step   {C_GREEN}[q]{RST} quit")
    else:
        lines.append(f"{C_GREEN}[Ctrl-C]{RST} quit   Running at {hz_val} Hz")

    sys.stdout.write(CLEAR + '\n'.join(lines) + '\n')
    sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rom")
    parser.add_argument("--step", action="store_true")
    parser.add_argument("--hz", type=float, default=4)
    args = parser.parse_args()

    if not os.path.exists(args.rom): sys.exit(1)
    rom_instructions = parse_rom(args.rom)
    cpu = ESTTA(rom_instructions)

    print(HIDE_CURSOR, end='')
    try:
        while True:
            render(cpu, rom_instructions, args.step, args.hz)
            if args.step:
                if input().lower() == 'q': break
            else:
                time.sleep(1.0 / args.hz)
            cpu.step()
    except KeyboardInterrupt: pass
    finally:
        print(SHOW_CURSOR)
        sys.stdout.write(CLEAR)
        print(f"\n{C_GREEN}ESTTA emulator stopped. {cpu.cycles} cycles executed.{RST}\n")

if __name__ == "__main__": main()