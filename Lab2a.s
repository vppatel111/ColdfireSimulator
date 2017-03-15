/* DO NOT MODIFY THIS --------------------------------------------*/
.text

.global AssemblyProgram

AssemblyProgram:
lea      -40(%a7),%a7 /*Backing up data and address registers */
movem.l %d2-%d7/%a2-%a5,(%a7)
/*----------------------------------------------------------------*/

/******************************************************************/
/* General Information ********************************************/
/* File Name: Lab2a.s *********************************************/
/* Names of Students: _________________ and ____________________ **/
/* Date: _________________                                       **/
/* General Description:                                          **/
/*                                                               **/
/******************************************************************/

/*Write your program here******************************************/


move.l	#0,(%a4)
/*Part A **********************************************************/
move.l  0x2300000,%d2 /* Size of each array */
move.l 	0x2300004,%a2 /* Array 1 */
move.l	0x2300008,%a3 /* Array 2 */
move.l	0x230000C,%a4 /* Array 1 + 2 */

move.l (%a2),%d4
move.l (%a3),%d5
add.l %d4,(%a4)
add.l %d5,(%a4)

move.l 4(%a2),%d4
move.l 4(%a3),%d5
add.l %d4,4(%a4)
add.l %d5,4(%a4)

move.l 8(%a2),%d4
move.l 8(%a3),%d5
add.l %d4,8(%a4)
add.l %d5,8(%a4)


/*Part B **********************************************************/
move.l	0x2300010,%a4 /* Array 1 + 2 */

clr.l	%d5 /* Indirect Counter */
move.l 	%d2,%d3


LoopB:
move.l 	(%a2,%d5),%d4
add.l 	%d4,(%a4,%d5)
move.l 	(%a3,%d5),%d4
add.l 	%d4,(%a4,%d5)

addi.l #4,%d5

sub.l 	#1,%d3 /* Subtract from coutner. */
beq 	DoneB
bra 	LoopB
DoneB:

/*Part C **********************************************************/
move.l	0x2300014,%a4 /* Array 1 + 2 */

move.l %d2,%d3

LoopC:
move.l 	(%a2)+,%d4
add.l 	%d4,(%a4)
move.l 	(%a3)+,%d5
add.l 	%d5,(%a4)+

sub.l #1,%d3 /* Subtract from coutner. */
beq DoneC /* if d3 is 0, end. Else loop. */
bra LoopC

DoneC:






/*End of program **************************************************/

/* DO NOT MODIFY THIS --------------------------------------------*/
movem.l (%a7),%d2-%d7/%a2-%a5 /*Restore data and address registers */
lea      40(%a7),%a7 
rts
/*----------------------------------------------------------------*/
