class Parser:
    def __init__(self):
        self.commandTypeDict = {"add": "C_ARITHMETIC",
                                "sub": "C_ARITHMETIC",
                                "neg": "C_ARITHMETIC",
                                "eq": "C_ARITHMETIC",
                                "gt": "C_ARITHMETIC",
                                "lt": "C_ARITHMETIC",
                                "and": "C_ARITHMETIC",
                                "or": "C_ARITHMETIC",
                                "not": "C_ARITHMETIC",
                                "push": "C_PUSH",
                                "pop": "C_POP",
                                "label": "C_LABEL",
                                "goto": "C_GOTO",
                                "if-goto": "C_IF",
                                "function": "C_FUNCTION",
                                "return": "C_RETURN",
                                "call": "C_CALL",
                                }
    def removeComments(self, line):
        line = line.split("//")[0]
        line = line.strip()
        return line

    def commandType(self, line):
        arg1 = line.split(" ")[0]
        return self.commandTypeDict[arg1]
    
    def arg0(self, line):
        return line.split(" ")[0]

    def arg1(self, line):
        return line.split(" ")[1]

    def arg2(self, line):
        return line.split(" ")[2]