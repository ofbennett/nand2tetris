class CodeWriter:
    def __init__(self, asmFile):
        self.asmFile = asmFile
    
    def writeArithmetic(self, command):
        asm = ""
        if command == "add":
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
                