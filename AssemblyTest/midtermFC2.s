MOVE.L #0x0000EEEE,%D3
MOVE.L #0,%D4
MOVEA.L   #0x0000EDCB,%A0
BMI JMP2
ADD.L #0x0011,%D3
JMP2: ADD.L #0x1100,%D3