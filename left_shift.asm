; Left Shift Library - Left shift by 1 bit (multiply by 2)
; 
; Usage:
;   move VALUE_TO_SHIFT REG6
;   include %left_shift.asm%
;   move REG7 DISPLAY1  ; result is in REG7
;
; How it works: x << 1 = x * 2 = x + x
; Uses only subtraction: x + x = x - (255 - x) = 2x (with wraparound)
; Uses REG6 (input), REG7 (output), REG8-REG9 (scratch)

; Load input value
move REG6 REG8                 ; REG8 = input value to shift

; Compute: INPUT - (255 - INPUT) = INPUT * 2
move CONSTANT_0 ALU_INPUT_A
move REG8 ALU_INPUT_B
move ALU_OUTPUT REG9           ; REG9 = 0 - INPUT = 255 - INPUT (via wraparound)

move REG8 ALU_INPUT_A
move REG9 ALU_INPUT_B
move ALU_OUTPUT REG7           ; REG7 = INPUT - (255 - INPUT) = 2 * INPUT

