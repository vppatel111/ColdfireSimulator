move.w #0x15, 0x1000
move.w #0x32, 0x1002
move.w #0x1, 0x1004
move.w #0xAA, 0x1006
move.w #0xFFFF, 0x1008

Start: 	clr.l %d0
	clr.l %d1
	movea.l #0x1000, %a0
	move.l #5, %d2

Loop:	move.w (%a0),%d3
	bpl Positive

Negative: add.l #1, %d1
	bra Check

Positive: add.l #1, %d0

Check:	adda.l #2, %a0
	sub.l #1, %d2
	bne Loop
