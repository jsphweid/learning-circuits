// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// R0 stores current white
// R1 stores current black
// R2 is max

@KBD
D=A

// FINAL
@R2
M=D

// TEMP -- just to test with smaller portions since a refresh takes an eternity on the CPU Emulator
// @SCREEN
// D=A
// @R2
// M=D+1
// @R2
// M=M+1


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



(EVAL)
  @KBD // store keyboard value in D
  D=M

  @PREPBLACK
  D;JGT

  @PREPWHITE
  0;JMP

  // @LOOP
  // 0;JMP