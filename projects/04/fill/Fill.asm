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

(KEY_CHECK_START)
// Check if key pressed
@KBD
D=M
@FILL_START
D;JNE
@CLEAR_START
D;JEQ

(KEY_CHECK_CONTINUE)
// Check if key pressed
@KBD
D=M
@FILL_CONTINUE
D;JNE
@CLEAR_CONTINUE
D;JEQ

(FILL_START)
@SCREEN
D=A
@current
M=D
(FILL_CONTINUE)
@current
A=M
M=-1
@current
M=M+1
D=M
@24576
D=A-D
@KEY_CHECK_START
D;JLE // Check if at end of screen
@KEY_CHECK_CONTINUE
0;JMP

(CLEAR_START)
@SCREEN
D=A
@current
M=D
(CLEAR_CONTINUE)
@current
A=M
M=0
@current
M=M+1
D=M
@24576
D=A-D
@KEY_CHECK_START
D;JLE // Check if at end of screen
@KEY_CHECK_CONTINUE
0;JMP
