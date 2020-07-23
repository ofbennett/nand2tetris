class Parser:
    def __init__(self,sourceFile):
        self.sourceFile = sourceFile
        self.rawLines = sourceFile.readlines()
        self.commandsWithLables = []
        self.commandsWithoutLables = []
        self.commandNum = 0
        self.currentCommandIndex = -1
        self.currentCommand = ""

    def removeCommentsAndWhiteSpace(self):
        for line in self.rawLines:
            if "//" in line:
                line = line.split("//")[0]
            line = line.strip()
            if len(line) > 0:
                self.commandsWithLables.append(line)
                self.commandNum += 1
        del self.rawLines
    
    def processLabels(self, symbolTable):
        currentIndex = 0
        for com in self.commandsWithLables:
            self.currentCommand = com
            if self.commandType() == "L_COMMAND":
                symbol = self.currentCommand[1:-1]
                symbolTable.addEntry(symbol, currentIndex)
            else:
                currentIndex += 1
                self.commandsWithoutLables.append(self.currentCommand)
        self.commandNum = currentIndex
    
    def hasMoreCommands(self):
        return self.currentCommandIndex + 1 < self.commandNum

    def advance(self):
        self.currentCommandIndex += 1
        self.currentCommand = self.commandsWithoutLables[self.currentCommandIndex]

    def commandType(self):
        com = self.currentCommand
        if com[0] == "(":
            return "L_COMMAND"
        elif com[0] == "@":
            return "A_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self):
        return self.currentCommand[1:]
    
    def dest(self):
        if "=" in self.currentCommand:
            return self.currentCommand.split("=")[0]
        else:
            return None
    
    def comp(self):
        comp = self.currentCommand.split(";")[0]
        if "=" in comp:
            comp = comp.split("=")[1]
        return comp
    
    def jump(self):
        if ";" in self.currentCommand:
            return self.currentCommand.split(";")[-1]
        else:
            return None
