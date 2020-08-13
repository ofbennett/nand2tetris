class VMWriter:

    segDict = {"CONST":"constant", "ARG":"argument", "VAR":"local", "STATIC":"static", "THIS":"this", "THAT":"that", "POINTER":"pointer", "TEMP":"temp"}

    def __init__(self, vmFile):
        self.vmFile = vmFile

    def writePush(self, segment, index):
        seg = VMWriter.segDict[segment]
        command = f"push {seg} {index}\n"
        self.vmFile.write(command)

    def writePop(self, segment, index):
        seg = VMWriter.segDict[segment]
        command = f"pop {seg} {index}\n"
        self.vmFile.write(command)

    def writeArithmetic(self, command):
        self.vmFile.write(command + "\n")

    def writeLabel(self, label):
        command = f"label {label}\n"
        self.vmFile.write(command)

    def writeGoto(self, label):
        command = f"goto {label}\n"
        self.vmFile.write(command)

    def writeIf(self, label):
        command = f"if-goto {label}\n"
        self.vmFile.write(command)

    def writeCall(self, name, nArgs):
        command = f"call {name} {nArgs}\n"
        self.vmFile.write(command)

    def writeFunction(self, name, nLocals):
        command = f"function {name} {nLocals}\n"
        self.vmFile.write(command)

    def writeReturn(self):
        command = "return\n"
        self.vmFile.write(command)
