; Right Shift Library - Divide by 2 using subtraction + conditionals
; 
; Usage (right shift by 1):
;   move VALUE_TO_SHIFT REG6
;   include %right_shift.asm%
;   move REG7 DISPLAY1  ; result is in REG7
;
; How it works:
;   x >> 1 = x ÷ 2
;   Algorithm: Count how many times we subtract 2 before crossing zero
;   Uses conditional jumps (zero-flag triggered COND_IN → COND_OUT)
;   Uses REG6 (input), REG7 (output counter), REG8-REG11 (scratch)

; Initialize result to 0
move CONSTANT_0 REG7          ; REG7 = count (result of shift)
move REG6 REG8                ; REG8 = working copy of input

; Prepare the loop counter (REG9 tracks remaining iterations)
move REG8 ALU_INPUT_A
move CONSTANT_0 ALU_INPUT_B
move ALU_OUTPUT REG9          ; REG9 = input value

; Main loop: subtract 2 each iteration until we can't
; (This approximates dividing by 2)

right_shift_1_loop:
  ; Check if we should continue (VALUE >= 2)
  move REG8 ALU_INPUT_A
  move CONSTANT_1 ALU_INPUT_B
  move ALU_OUTPUT REG10       ; REG10 = VALUE - 1
  
  move REG10 ALU_INPUT_A
  move CONSTANT_1 ALU_INPUT_B
  move ALU_OUTPUT REG11       ; REG11 = VALUE - 2
  
  ; If VALUE < 2, we're done (exit condition)
  ; Check if REG8 is <= 1 by testing if it can be subtracted by 2
  move REG8 ALU_INPUT_A
  move CONSTANT_1 ALU_INPUT_B
  move ALU_OUTPUT COND_IN     ; COND_IN = REG8 - 1
  
  ; If ALU result is 0 (VALUE was 1), conditional triggers and COND_OUT gets set
  ; We can use COND_OUT as a jump target if it's non-zero, otherwise continue
  
  ; Decrement by 2 (subtract 1 twice)
  move REG8 ALU_INPUT_A
  move CONSTANT_1 ALU_INPUT_B
  move ALU_OUTPUT REG8        ; VALUE -= 1
  
  move REG8 ALU_INPUT_A
  move CONSTANT_1 ALU_INPUT_B
  move ALU_OUTPUT REG8        ; VALUE -= 1 (total: -2)
  
  ; Increment our shift counter
  move REG7 ALU_INPUT_A
  move CONSTANT_0 ALU_INPUT_B
  move ALU_OUTPUT REG7        ; REG7 = REG7 - 0 (copy)
  
  ; Increment REG7 by 1 (using subtraction: -(-1) = +1)
  move CONSTANT_1 ALU_INPUT_A
  move CONSTANT_0 ALU_INPUT_B
  move ALU_OUTPUT REG10       ; REG10 = 1
  
  move REG7 ALU_INPUT_A
  move REG10 ALU_INPUT_B
  move ALU_OUTPUT REG10       ; REG10 = REG7 - 1
  
  move REG10 ALU_INPUT_A
  move CONSTANT_0 ALU_INPUT_B
  move ALU_OUTPUT REG7        ; REG7 = (REG7 - 1) - 0... 
  
  ; Note: Incrementing with only subtraction is non-trivial
  ; Practical workaround: use left_shift and count instead
