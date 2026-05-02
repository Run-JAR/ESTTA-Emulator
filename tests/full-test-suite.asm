include %reg_names.asm%

move CONSTANT_1 REG6
include %left_shift.asm%
move REG7 REG10
move CONSTANT_1 REG6
include %addition.asm%
move REG8 REG6
move REG10 REG7
include %addition.asm%
move REG8 DISPLAY1
move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY2