class VMWriter:

    segDict = {"CONST":"constant", "ARG":"argument", "LOCAL":"local", "STATIC":"static", "THIS":"this", "THAT":"that", "POINTER":"pointer", "TEMP":"temp"}

    def __init__(self, vmFile):
        self.vmFile = vmFile

    def writePush(self, segment, index):
        seg = VMWriter.segDict[segment]
        command = f"push {seg} {index}"
        self.vmFile.write(command)

    def writePop(self, segment, index):
        seg = VMWriter.segDict[segment]
        command = f"pop {seg} {index}"
        self.vmFile.write(command)

    def writeArithmetic(self, command):
        command = command.lower()
        self.vmFile.write(command)

    def writeLabel(self, label):
        command = f"({label})"
        self.vmFile.write(command)

    def writeGoto(self, label):
        command = f"goto {label}"
        self.vmFile.write(command)

    def writeIf(self, label):
        command = f"if-goto {label}"
        self.vmFile.write(command)

    def writeCall(self, name, nArgs):
        command = f"call {name} {nArgs}"
        self.vmFile.write(command)

    def writeFunction(self, name, nLocals):
        command = f"function {name} {nLocals}"
        self.vmFile.write(command)

    def writeReturn(self):
        command = "return"
        self.vmFile.write(command)
