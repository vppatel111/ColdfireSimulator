move.l  #0xFFFEDCBF,%d0
move.l  #0x12348765,%d1
move.l  #0x8070A0B0,%a0
move.b	%d1,%d0
move.w	%d0,%d1
move.l	(%a2)+,(%a1)
move.l	%d0,(%a1)
move.l	-(%a3),(%a2)
move.l  (3, %a0, %d1),-(%a1)
