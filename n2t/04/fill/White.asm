@SCREEN
D=A
@curr
M=D

(LOOP)
  @curr
  A=M
  M=0
  @curr
  M=M+1

  @KBD
  D=A

  @LOOP
  0;JMP


(END)
  @END
  0;JMP