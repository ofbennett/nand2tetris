from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    ops = set(["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="])
    tokTypeDict = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier", "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}

    def __init__(self, sourceFile, tokenFile, parseTreeFile, vmFile):
        self.sourceFile = sourceFile
        self.tokenFile = tokenFile
        self.parseTreeFile = parseTreeFile
        self.vmFile = vmFile
        self.tokenizer = JackTokenizer(sourceFile)
        self._createDebugTokenXML()
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(vmFile)

    def _createDebugTokenXML(self):
        debugTokenizer = JackTokenizer(self.sourceFile)
        self.tokenFile.write("<tokens>\n")
        while debugTokenizer.hasMoreTokens():
            tokType = debugTokenizer.tokenType()
            self.tokenFile.write(f"<{CompilationEngine.tokTypeDict[tokType]}> ")
            if tokType == "KEYWORD":
                tok = debugTokenizer.keyWord()
            elif tokType == "SYMBOL":
                tok = debugTokenizer.symbol()
            elif tokType == "IDENTIFIER":
                tok = debugTokenizer.identifier()
            elif tokType == "INT_CONST":
                tok = debugTokenizer.intVal()
            elif tokType == "STRING_CONST":
                tok = debugTokenizer.stringVal()
            self.tokenFile.write(tok)
            self.tokenFile.write(f" </{CompilationEngine.tokTypeDict[tokType]}>\n")
            debugTokenizer.advance()
        self.tokenFile.write("</tokens>")

    def writeTerminal(self, defined = False):
        extraInfo = ""
        tokType = self.tokenizer.tokenType()
        self.parseTreeFile.write(f"<{CompilationEngine.tokTypeDict[tokType]}> ")
        if tokType == "KEYWORD":
            tok = self.tokenizer.keyWord()
        elif tokType == "SYMBOL":
            tok = self.tokenizer.symbol()
        elif tokType == "IDENTIFIER":
            tok = self.tokenizer.identifier()
            if self.symbolTable.typeOf(tok) == "NONE":
                extraInfo = ".classOrSubroutine"
            else:
                extraInfo = f".{self.symbolTable.typeOf(tok)}.{self.symbolTable.kindOf(tok)}.{self.symbolTable.indexOf(tok)}"
                if defined:
                    extraInfo += ".defined"
                else:
                    extraInfo += ".used"
        elif tokType == "INT_CONST":
            tok = self.tokenizer.intVal()
        elif tokType == "STRING_CONST":
            tok = self.tokenizer.stringVal()
        self.parseTreeFile.write(tok + extraInfo)
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
        kind = self.tokenizer.keyWord().upper()
        varType = self.tokenizer.lookAheadOne()
        self.parseTreeFile.write("<classVarDec>\n")
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            if self.tokenizer.tokenType() == "IDENTIFIER":
                name = self.tokenizer.identifier()
                self.symbolTable.define(name, varType, kind)
                self.writeTerminal(defined=True)
            else:
                self.writeTerminal()
        self.parseTreeFile.write("</classVarDec>\n")

    def compileSubroutine(self):
        self.symbolTable.startSubroutine()
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
        kind = "ARG"
        n = 1
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ")":
                    break
            if n%3 == 1:
                if self.tokenizer.tokenType() == "KEYWORD":
                    varType = self.tokenizer.keyWord()
                    self.writeTerminal()
                else:
                    varType = self.tokenizer.identifier()
                    self.writeTerminal()
            elif n%3 == 2:
                name = self.tokenizer.identifier()
                self.symbolTable.define(name, varType, kind)
                self.writeTerminal(defined=True)
            elif n%3 == 0:
                self.writeTerminal()
                n = 0
            n += 1 
        self.parseTreeFile.write("</parameterList>\n")

    def compileVarDec(self):
        self.parseTreeFile.write("<varDec>\n")
        kind = "VAR"
        varType = self.tokenizer.lookAheadOne()
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self.writeTerminal()
                    break
            if self.tokenizer.tokenType() == "IDENTIFIER":
                name = self.tokenizer.identifier()
                self.symbolTable.define(name, varType, kind)
                self.writeTerminal(defined=True)
            else:
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
