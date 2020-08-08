from JackTokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, sourceFile, parsedFile):
        self.parsedFile = parsedFile
        self.tokenizer = JackTokenizer(sourceFile)

    def writeTerminal(self):
        tokTypeDict = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier", "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}
        tokType = self.tokenizer.tokenType()
        self.parsedFile.write(f"<{tokTypeDict[tokType]}> ")
        if tokType == "KEYWORD":
            tok = self.tokenizer.keyWord()
        elif tokType == "SYMBOL":
            tok = self.tokenizer.symbol()
        elif tokType == "IDENTIFIER":
            tok = self.tokenizer.identifier()
        elif tokType == "INT_CONST":
            tok = self.tokenizer.intVal()
        elif tokType == "STRING_CONST":
            tok = self.tokenizer.stringVal()
        self.parsedFile.write(tok)
        self.parsedFile.write(f" </{tokTypeDict[tokType]}>\n")
        self.tokenizer.advance()

    def compileClass(self):
        self.parsedFile.write("<class>\n")
        while self.tokenizer.hasMoreTokens():
            if self.tokenizer.tokenType() == "KEYWORD":
                if self.tokenizer.keyWord() in ["static", "field"]:
                    self.compileClassVarDec()
                if self.tokenizer.keyWord() in ["constructor", "function", "method"]:
                    self.compileSubroutine()
            self.writeTerminal()
        self.parsedFile.write("</class>")

    def compileClassVarDec(self):
        self.parsedFile.write("<classVarDec>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            self.writeTerminal()
        self.parsedFile.write("</classVarDec>\n")

    def compileSubroutine(self):
        self.parsedFile.write("<subroutineDec>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "(":
                    self.writeTerminal()
                    self.compileParameterList()
                    self.writeTerminal()
                    self.parsedFile.write("<subroutineBody>\n")
            if self.tokenizer.tokenType() == "KEYWORD":
                if self.tokenizer.keyWord() == "var":
                    self.compileVarDec()
            if self.tokenizer.tokenType() == "KEYWORD":
                if self.tokenizer.keyWord() in ["let", "if", "while", "do", "return"]:
                    self.compileStatements()
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "}":
                    self.writeTerminal()
                    break     
            self.writeTerminal()
        self.parsedFile.write("</subroutineBody>\n")
        self.parsedFile.write("</subroutineDec>\n")

    def compileParameterList(self):
        self.parsedFile.write("<parameterList>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ")":
                    break
            self.writeTerminal()
        self.parsedFile.write("</parameterList>\n")

    def compileVarDec(self):
        self.parsedFile.write("<varDec>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            self.writeTerminal()
        self.parsedFile.write("</varDec>\n")

    def compileStatements(self):
        self.parsedFile.write("<statements>\n")
        while True:
            if self.tokenizer.tokenType() == "KEYWORD":
                if self.tokenizer.keyWord() == "let":
                    self.compileLet()
                if self.tokenizer.keyWord() == "if":
                    self.compileIf()
                if self.tokenizer.keyWord() == "while":
                    self.compileWhile()
                if self.tokenizer.keyWord() == "do":
                    self.compileDo()
                if self.tokenizer.keyWord() == "return":
                    self.compileReturn()
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "}":
                    break
        self.parsedFile.write("</statements>\n")

    def compileDo(self):
        pass

    def compileLet(self):
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass

    def CompileExpression(self):
        pass

    def CompileTerm(self):
        pass

    def CompileExpressionList(self):
        pass