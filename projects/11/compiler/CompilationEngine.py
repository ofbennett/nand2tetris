from JackTokenizer import JackTokenizer

class CompilationEngine:
    ops = set(["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="])
    tokTypeDict = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier", "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}

    def __init__(self, sourceFile, parseTreeFile):
        self.parseTreeFile = parseTreeFile
        self.tokenizer = JackTokenizer(sourceFile)

    def writeTerminal(self):
        tokType = self.tokenizer.tokenType()
        self.parseTreeFile.write(f"<{CompilationEngine.tokTypeDict[tokType]}> ")
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
        self.parseTreeFile.write(tok)
        self.parseTreeFile.write(f" </{CompilationEngine.tokTypeDict[tokType]}>\n")
        self.tokenizer.advance()

    def compileClass(self):
        self.parseTreeFile.write("<class>\n")
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
        self.parseTreeFile.write("</class>")

    def compileClassVarDec(self):
        self.parseTreeFile.write("<classVarDec>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            self.writeTerminal()
        self.parseTreeFile.write("</classVarDec>\n")

    def compileSubroutine(self):
        self.parseTreeFile.write("<subroutineDec>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "(":
                    self.writeTerminal()
                    self.compileParameterList()
                    self.writeTerminal()
                    self.parseTreeFile.write("<subroutineBody>\n")
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
        self.parseTreeFile.write("</subroutineBody>\n")
        self.parseTreeFile.write("</subroutineDec>\n")

    def compileParameterList(self):
        self.parseTreeFile.write("<parameterList>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ")":
                    break
            self.writeTerminal()
        self.parseTreeFile.write("</parameterList>\n")

    def compileVarDec(self):
        self.parseTreeFile.write("<varDec>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            self.writeTerminal()
        self.parseTreeFile.write("</varDec>\n")

    def compileStatements(self):
        self.parseTreeFile.write("<statements>\n")
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
        self.parseTreeFile.write("</statements>\n")

    def compileDo(self):
        self.parseTreeFile.write("<doStatement>\n")
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
        self.parseTreeFile.write("</doStatement>\n")

    def compileLet(self):
        self.parseTreeFile.write("<letStatement>\n")
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
        self.parseTreeFile.write("</letStatement>\n")

    def compileWhile(self):
        self.parseTreeFile.write("<whileStatement>\n")
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
        self.parseTreeFile.write("</whileStatement>\n")

    def compileReturn(self):
        self.parseTreeFile.write("<returnStatement>\n")
        self.writeTerminal()
        if self.tokenizer.tokenType() == "SYMBOL":
            if self.tokenizer.symbol() == ";":
                self.writeTerminal()
                self.parseTreeFile.write("</returnStatement>\n")
                return
        self.compileExpression(endTokens = [";"])
        self.writeTerminal()
        self.parseTreeFile.write("</returnStatement>\n")

    def compileIf(self):
        self.parseTreeFile.write("<ifStatement>\n")
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
        self.parseTreeFile.write("</ifStatement>\n")

    def compileExpression(self, endTokens):
        self.parseTreeFile.write("<expression>\n")
        self.compileTerm()
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() in endTokens:
                    break
                elif self.tokenizer.symbol() in CompilationEngine.ops:
                    self.writeTerminal()
                else:
                    self.compileTerm()
            else:
                self.compileTerm()
        self.parseTreeFile.write("</expression>\n")

    def compileTerm(self):
        self.parseTreeFile.write("<term>\n")
        if self.tokenizer.tokenType() == "SYMBOL":
            if self.tokenizer.symbol() in ["-", "~"]:
                 self.writeTerminal()
                 self.compileTerm()
            elif self.tokenizer.symbol() == "(":
                self.writeTerminal()
                self.compileExpression(endTokens = [")"])
                self.writeTerminal()
        elif self.tokenizer.tokenType() in ["KEYWORD", "STRING_CONST", "INT_CONST"]:
            self.writeTerminal()
        elif self.tokenizer.tokenType() == "IDENTIFIER":
            if self.tokenizer.lookAheadOne() in ["(","."]:
                self.compileSubroutineCall()
            elif self.tokenizer.lookAheadOne() == "[":
                self.writeTerminal()
                self.writeTerminal()
                self.compileExpression(endTokens = ["]"])
                self.writeTerminal()
            else:
                self.writeTerminal()
        self.parseTreeFile.write("</term>\n")

    def compileSubroutineCall(self):
        self.writeTerminal()
        if self.tokenizer.tokenType() == "SYMBOL":
            if self.tokenizer.symbol() == "(":
                self.writeTerminal()
                self.compileExpressionList()
                self.writeTerminal()
            elif self.tokenizer.symbol() == ".":
                self.writeTerminal()
                self.writeTerminal()
                self.writeTerminal()
                self.compileExpressionList()
                self.writeTerminal()
            else:
                raise Exception("Should never reach here")

    def compileExpressionList(self):
        self.parseTreeFile.write("<expressionList>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ",":
                    self.writeTerminal()
                if self.tokenizer.symbol() == ")":
                    break
            self.compileExpression(endTokens = [",",")"])
        self.parseTreeFile.write("</expressionList>\n")
