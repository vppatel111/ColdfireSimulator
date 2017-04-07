Start: 	clr.l %d0
	clr.l %d1
	movea.l #0x1000, %a0
	move.l #5, %d2
	move.l #2, %d2
	add.l #2, %d2
Loop:	move.w (%a0),%d3
	bpl Positive

Negative: add.l #1, %d1
	bra Check

Positive:
	add.l #1, %d0
Check:	adda.l #2, %a0
	sub.l #1, %d2
	bne Loop
