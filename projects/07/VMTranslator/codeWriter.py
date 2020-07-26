from collections import Counter

class CodeWriter:
    def __init__(self, asmFile):
        self.asmFile = asmFile
        self.prevArithCommands = Counter()

    def writeArithmetic(self, command):
        asm = ""
        if command == "neg":
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "M=-M\n"
        
        elif command == "not":
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "M=!M\n"

        elif command == "add":
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=D+M\n"
            asm += "M=D\n"
            asm += "A=A+1\n"
            asm += "D=A\n"
            asm += "@SP\n"
            asm += "M=D\n"
        
        elif command == "and":
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=D&M\n"
            asm += "M=D\n"
            asm += "A=A+1\n"
            asm += "D=A\n"
            asm += "@SP\n"
            asm += "M=D\n"
        
        elif command == "or":
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=D|M\n"
            asm += "M=D\n"
            asm += "A=A+1\n"
            asm += "D=A\n"
            asm += "@SP\n"
            asm += "M=D\n"
        
        elif command == "sub":
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=M-D\n"
            asm += "M=D\n"
            asm += "A=A+1\n"
            asm += "D=A\n"
            asm += "@SP\n"
            asm += "M=D\n"

        elif command == "eq":
            comNum = self.prevArithCommands[command]

            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=D-M\n" # Check for equality here

            # Branching here
            asm += f"@EQ_EQUAL_{comNum}\n"
            asm += "D;JEQ\n"
            asm += f"@EQ_NOT_EQUAL_{comNum}\n"
            asm += "0;JMP\n"
            
            # If equal do this
            asm += f"(EQ_EQUAL_{comNum})\n"
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "A=A-1\n"
            asm += "M=-1\n"
            asm += f"@EQ_RESET_SP_{comNum}\n"
            asm += "0;JMP\n"

            # If not equal do this
            asm += f"(EQ_NOT_EQUAL_{comNum})\n"
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "A=A-1\n"
            asm += "M=0\n"

            # Reset stack pointer and end
            asm += f"(EQ_RESET_SP_{comNum})\n"
            asm += "@SP\n"
            asm += "M=M-1\n"
        
        elif command == "lt":
            comNum = self.prevArithCommands[command]

            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=D-M\n" # Compare values here

            # Branching here
            asm += f"@LT_LT_{comNum}\n"
            asm += "D;JGT\n"
            asm += f"@LT_NOT_LT_{comNum}\n"
            asm += "0;JMP\n"
            
            # If less than do this
            asm += f"(LT_LT_{comNum})\n"
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "A=A-1\n"
            asm += "M=-1\n"
            asm += f"@LT_RESET_SP_{comNum}\n"
            asm += "0;JMP\n"

            # If not less than do this
            asm += f"(LT_NOT_LT_{comNum})\n"
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "A=A-1\n"
            asm += "M=0\n"

            # Reset stack pointer and end
            asm += f"(LT_RESET_SP_{comNum})\n"
            asm += "@SP\n"
            asm += "M=M-1\n"
        
        elif command == "gt":
            comNum = self.prevArithCommands[command]

            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=M-D\n" # Compare values here

            # Branching here
            asm += f"@GT_GT_{comNum}\n"
            asm += "D;JGT\n"
            asm += f"@GT_NOT_GT_{comNum}\n"
            asm += "0;JMP\n"
            
            # If greater than do this
            asm += f"(GT_GT_{comNum})\n"
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "A=A-1\n"
            asm += "M=-1\n"
            asm += f"@GT_RESET_SP_{comNum}\n"
            asm += "0;JMP\n"

            # If not greater than do this
            asm += f"(GT_NOT_GT_{comNum})\n"
            asm += "@SP\n"
            asm += "A=M\n"
            asm += "A=A-1\n"
            asm += "A=A-1\n"
            asm += "M=0\n"

            # Reset stack pointer and end
            asm += f"(GT_RESET_SP_{comNum})\n"
            asm += "@SP\n"
            asm += "M=M-1\n"
   
        self.prevArithCommands[command] += 1
        self.asmFile.write(asm)

    def writePushPop(self, command, segment, index):
        asm = ""
        if command == "push":
            if segment == "constant":
                asm += f"@{index}\n"
                asm += "D=A\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n"
        self.asmFile.write(asm)
                