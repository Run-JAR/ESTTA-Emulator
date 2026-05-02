include %reg_names.asm%

move PC REG10
move CONSTANT_1 DISPLAY2

;----MOVE ACROSS DISPLAY2----

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

;1 EXTRA TO CLEAR DISPLAY

move DISPLAY2 REG6
include %left_shift.asm%
move REG7 DISPLAY2

;----MOVE ACROSS DISPLAY1----

move CONSTANT_1 DISPLAY1
move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

move DISPLAY1 REG6
include %left_shift.asm%
move REG7 DISPLAY1

;JUMP BACK TO START
move REG10 PC