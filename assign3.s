move.l	#0xABECE212,%d0
move.l	#0x1000, %a0

move.b	#0x55, 0x1000
move.b	#0x66, 0x1001
move.b	#0x77, 0x1002
move.b	#0x88, 0x1003

move.w (%a0),%d0
move.l %d0, 0x1001
move.l %d0, 0x1004
