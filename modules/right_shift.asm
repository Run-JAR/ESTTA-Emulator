; Right Shift Library - Improved (Divide by 2)
;
; Strategy: The logical inverse of left_shift.asm (x+x).
; We subtract 2 from the input and add 1 to the result repeatedly.
; This uses no extra defines and follows the patterns in left_shift.asm.

; Setup
move CONSTANT_0 REG7           ; REG7 = Result (starts at 0)
move REG6 REG8                 ; REG8 = Input to shift

; Identity from left_shift.asm: To add 1, we subtract (0 - 1)
move CONSTANT_0 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG9           ; REG9 = -1 (0xFF)

; --- Step 1 ---
; Subtract 2 from input (REG8)
move REG8 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG10
move REG10 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG8           ; REG8 = Input - 2

; Add 1 to result (REG7) using left_shift logic: REG7 = REG7 - (-1)
move REG7 ALU_INPUT_A
move REG9 ALU_INPUT_B
move ALU_OUTPUT REG7           ; REG7 = 1

; --- Step 2 ---
move REG8 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG10
move REG10 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG8
move REG7 ALU_INPUT_A
move REG9 ALU_INPUT_B
move ALU_OUTPUT REG7           ; REG7 = 2

; --- Step 3 ---
move REG8 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG10
move REG10 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG8
move REG7 ALU_INPUT_A
move REG9 ALU_INPUT_B
move ALU_OUTPUT REG7           ; REG7 = 3

; --- Step 4 ---
move REG8 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG10
move REG10 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG8
move REG7 ALU_INPUT_A
move REG9 ALU_INPUT_B
move ALU_OUTPUT REG7           ; REG7 = 4

; --- Step 5 ---
move REG8 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG10
move REG10 ALU_INPUT_A
move CONSTANT_1 ALU_INPUT_B
move ALU_OUTPUT REG8
move REG7 ALU_INPUT_A
move REG9 ALU_INPUT_B
move ALU_OUTPUT REG7           ; REG7 = 5