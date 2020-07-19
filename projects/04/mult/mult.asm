// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@i
M=0 // i=0

@sum
M=0 // sum=0

@2
M=0 // prod=0

(LOOP)

// Check if i>R1, if so end loop
@i
D=M
@1
D=M-D
@ENDLOOP
D;JLE

// Increase sum by R0
@sum
D=M
@0
D=D+M
@sum
M=D

@i
M=M+1 // i++

@LOOP
0;JMP
(ENDLOOP)

// Assign R2 to final prod value
@sum
D=M
@2
M=D

// End program
(END)
@END
0;JMP
