// Put your code here.

// R0 stores current white
// R1 stores current black
// R2 is max

@KBD
D=A
@R2
M=D

(EVAL)
  @KBD // store keyboard value in D
  D=M

  @PREPBLACK
  D;JGT

  @PREPWHITE
  0;JMP

(WHITE)
  @R2 // if we've reached kbd, go back to eval loop
  D=M
  @R0
  D=M-D
  @EVAL
  D;JEQ

  @R0 // paint
  A=M
  M=0

  @R0 // increment
  M=M+1
  
  @WHITE
  0;JMP


(BLACK)
  @R2 // if we've reached kbd, go back to eval loop
  D=M
  @R1
  D=M-D
  @EVAL
  D;JEQ

  @R1 // paint
  A=M
  M=-1

  @R1 // increment
  M=M+1

  @BLACK
  0;JMP


(PREPWHITE)
  @SCREEN
  D=A
  @R0
  M=D

  @WHITE
  0;JMP


(PREPBLACK)
  @SCREEN
  D=A
  @R1
  M=D

  @BLACK
  0;JMP
