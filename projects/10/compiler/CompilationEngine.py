from JackTokenizer import JackTokenizer

class CompilationEngine:
    ops = set(["+", "-", "*", "/", "&", "|", "<", ">", "="])
    tokTypeDict = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier", "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}

    def __init__(self, sourceFile, parsedFile):
        self.parsedFile = parsedFile
        self.tokenizer = JackTokenizer(sourceFile)

    def writeTerminal(self):
        tokType = self.tokenizer.tokenType()
        self.parsedFile.write(f"<{CompilationEngine.tokTypeDict[tokType]}> ")
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
        # print(tok)
        self.parsedFile.write(f" </{CompilationEngine.tokTypeDict[tokType]}>\n")
        self.tokenizer.advance()

    def compileClass(self):
        self.parsedFile.write("<class>\n")
        while self.tokenizer.hasMoreTokens():
            if self.tokenizer.tokenType() == "KEYWORD":
                if self.tokenizer.keyWord() in ["static", "field"]:
                    self.compileClassVarDec()
                elif self.tokenizer.keyWord() in ["constructor", "function", "method"]:
                    self.compileSubroutine()
                else:
                    self.writeTerminal()    
            else:
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
                elif self.tokenizer.symbol() == "}":
                    self.writeTerminal()
                    break
                else:    
                    self.writeTerminal()
            elif self.tokenizer.tokenType() == "KEYWORD":
                if self.tokenizer.keyWord() == "var":
                    self.compileVarDec()
                elif self.tokenizer.keyWord() in ["let", "if", "while", "do", "return"]:
                    self.compileStatements()
                else:    
                    self.writeTerminal()
            else:    
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
        self.parsedFile.write("<doStatement>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "(":
                    self.writeTerminal()
                    self.compileExpressionList()
                    self.writeTerminal()
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            self.writeTerminal()
        self.parsedFile.write("</doStatement>\n")

    def compileLet(self):
        self.parsedFile.write("<letStatement>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "[":
                    self.writeTerminal()
                    self.compileExpression(endTokens = ["]"])
                    self.writeTerminal()
                if self.tokenizer.symbol() == "=":
                    self.writeTerminal()
                    self.compileExpression(endTokens = [";"])
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            self.writeTerminal()
        self.parsedFile.write("</letStatement>\n")

    def compileWhile(self):
        self.parsedFile.write("<whileStatement>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "(":
                    self.writeTerminal()
                    self.compileExpression(endTokens = [")"])
                    self.writeTerminal()
                if self.tokenizer.symbol() == "{":
                    self.writeTerminal()
                    self.compileStatements()
                    self.writeTerminal()
                    break
            self.writeTerminal()
        self.parsedFile.write("</whileStatement>\n")

    def compileReturn(self):
        self.parsedFile.write("<returnStatement>\n")
        self.writeTerminal()
        if self.tokenizer.tokenType() == "SYMBOL":
            if self.tokenizer.symbol() == ";":
                self.writeTerminal()
                self.parsedFile.write("</returnStatement>\n")
                return
        self.compileExpression(endTokens = [";"])
        self.writeTerminal()
        self.parsedFile.write("</returnStatement>\n")

    def compileIf(self):
        self.parsedFile.write("<ifStatement>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "(":
                    self.writeTerminal()
                    self.compileExpression(endTokens = [")"])
                    self.writeTerminal()
                if self.tokenizer.symbol() == "{":
                    self.writeTerminal()
                    self.compileStatements()
                    self.writeTerminal()
                    if self.tokenizer.tokenType() == "KEYWORD":
                        if self.tokenizer.symbol() == "else":
                            continue
                        else:
                            break
                    else:
                        break
            self.writeTerminal()
        self.parsedFile.write("</ifStatement>\n")

    def compileExpression(self, endTokens):
        self.parsedFile.write("<expression>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() in endTokens:
                    break
                if self.tokenizer.symbol() in CompilationEngine.ops:
                    self.writeTerminal()
            self.compileTerm()
        self.parsedFile.write("</expression>\n")

    def compileTerm(self):
        self.parsedFile.write("<term>\n")
        self.writeTerminal()
        self.parsedFile.write("</term>\n")

    def compileExpressionList(self):
        self.parsedFile.write("<expressionList>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ",":
                    self.writeTerminal()
                if self.tokenizer.symbol() == ")":
                    break
            self.compileExpression(endTokens = [",",")"])
        self.parsedFile.write("</expressionList>\n")