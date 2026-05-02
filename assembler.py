import sys
import os
import re

def preprocess_files(filename, include_stack=None):
    """Recursively reads files and handles 'include %filename%' directives."""
    if include_stack is None:
        include_stack = []
    
    # Prevent infinite loops (circular includes only)
    abs_path = os.path.abspath(filename)
    if abs_path in include_stack:
        print(f"Warning: Circular include detected for {filename}. Skipping.")
        return []
    
    include_stack.append(abs_path)
    
    if not os.path.exists(filename):
        print(f"Error: Included file '{filename}' not found.")
        include_stack.pop()
        return []
    
    all_lines = []
    with open(filename, 'r') as f:
        for line in f:
            # Match pattern: include %filename.asm%
            match = re.match(r"^\s*include\s+%(.*)%", line, re.IGNORECASE)
            if match:
                included_filename = match.group(1).strip()
                # Recursively get lines from the included file
                all_lines.extend(preprocess_files(included_filename, include_stack))
            else:
                all_lines.append(line)
    
    include_stack.pop()
    return all_lines

def assemble(input_file, output_file):
    # Use the new preprocessor instead of a simple f.readlines()
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    lines = preprocess_files(input_file)
    if not lines:
        return

    symbols = {} 
    text_rom_chunks = []
    instruction_count = 0
    
    print(f"\nAssembling: {input_file}")
    print(f"{'Addr':<6} | {'Instruction':<25} | {'16-bit Pattern'}")
    print("-" * 75)

    for line_num, line in enumerate(lines, 1):
        # 1. Strip comments and whitespace
        clean = re.sub(r';.*', '', line).strip()
        if not clean:
            continue
        
        parts = clean.replace(',', ' ').split()
        cmd = parts[0].lower()

        # 2. Map your Defines: define <VAL> <NAME>
        if cmd == 'define' and len(parts) >= 3:
            val = parts[1]
            name = parts[2].lower()
            symbols[name] = val
            continue

        # 3. Process Moves: move <SRC> <DEST>
        if cmd == 'move' and len(parts) >= 3:
            try:
                src_raw = symbols.get(parts[1].lower(), parts[1])
                dest_raw = symbols.get(parts[2].lower(), parts[2])

                src_val = int(src_raw, 16) & 0xF
                dest_val = int(dest_raw, 16) & 0xF

                src_bin = format(src_val, '04b')[::-1]
                dest_bin = format(dest_val, '04b')
                
                padding = "00000000"
                full_chunk = f"{padding}{src_bin}{dest_bin}"
                text_rom_chunks.append(full_chunk)
                
                print(f"[{instruction_count:<3}] | {clean[:25]:<25} | {padding} {src_bin} {dest_bin}")
                instruction_count += 1
                
            except Exception as e:
                print(f"Line {line_num} Error: {e}")

    # 4. Save output
    if text_rom_chunks:
        with open(output_file, 'w') as f:
            f.write("\n".join(text_rom_chunks))
        print(f"\nSuccess! Created {output_file}")
    else:
        print("\nError: No valid instructions found.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python assembler.py input.asm")
    else:
        infile = sys.argv[1]
        outfile = os.path.splitext(infile)[0] + '.rom'
        assemble(infile, outfile)