Start: 	clr.l %d0
	clr.l %d1
	movea.l #0x2000, %a0
	move.l #100, (%a0)
	move.l (%a0), %d7
	move.l #5, %d2
	move.l #2, %d2
	add.l #2, %d2
	addi.l #2, %d2
	adda.l #2, %a0
	clr.l %d2
	pea 0x1000
	lea 0x1000, %a1
	sub.l #3, %d2
	sub.l #20, %d2
	move.l #4, (%a0)
	move.l #5, 0x1000
	move.l #20, 0x1000
	move.l #5, 0x1000
lea 0x1000, %a1
	sub.l #3, %d2
sub.l #20, %d2
move.l #4, (%a0)
	move.l #5, 0x1000
move.l #20, 0x1000
	move.l #5, 0x1000
Loop:	move.w (%a0),%d3
	bpl Positive

Negative: add.l #1, %d1
	bra Check

Positive:
	add.l #1, %d0
Check:	adda.l #2, %a0
	sub.l #1, %d2
	bne Loop
