from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    ops = set(["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="])
    vmOps = {"+": "add", "-": "sub", "*": "call Math.multiply 2", "/": "call Math.divide 2", "&amp;": "and", "|": "or", "&lt;": "lt", "&gt;": "gt", "=": "eq"}
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
        self.nWhile = 0
        self.nIf = 0

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
        extraInfo = ""
        self.parseTreeFile.write(tok + extraInfo)
        self.parseTreeFile.write(f" </{CompilationEngine.tokTypeDict[tokType]}>\n")
        self.tokenizer.advance()

    def compileClass(self):
        self.parseTreeFile.write("<class>\n")
        self.className = self.tokenizer.lookAheadOne()
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
        self.writeTerminal()
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
        nLocals = 0
        nLocalsCompiled = False
        self.parseTreeFile.write("<subroutineDec>\n")
        self.funcType = self.tokenizer.keyWord()
        self.writeTerminal()
        funcName = self.tokenizer.lookAheadOne()
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
                    nNewLocals = self.compileVarDec()
                    nLocals += nNewLocals
                elif self.tokenizer.keyWord() in ["let", "if", "while", "do", "return"]:
                    if not nLocalsCompiled:
                        self.vmWriter.writeFunction(f"{self.className}.{funcName}", nLocals)
                        if self.funcType == "method":
                            self.vmWriter.writePush("ARG", 0)
                            self.vmWriter.writePop("POINTER", 0)
                        elif self.funcType == "constructor":
                            nFields = self.symbolTable.varCount("FIELD")
                            self.vmWriter.writePush("CONST", nFields)
                            self.vmWriter.writeCall("Memory.alloc", 1)
                            self.vmWriter.writePop("POINTER", 0)
                        nLocalsCompiled = True
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
        nNewVars = 0
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
                nNewVars += 1
                self.writeTerminal(defined=True)
            else:
                self.writeTerminal()
        self.parseTreeFile.write("</varDec>\n")
        return nNewVars

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
        self.writeTerminal()
        self.compileSubroutineCall()
        self.writeTerminal()
        self.vmWriter.writePop("TEMP", 0)
        self.parseTreeFile.write("</doStatement>\n")

    def compileLet(self):
        self.parseTreeFile.write("<letStatement>\n")
        self.writeTerminal()
        kind = self.symbolTable.kindOf(self.tokenizer.identifier())
        index = self.symbolTable.indexOf(self.tokenizer.identifier())
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
        if kind == "FIELD":
            kind = "THIS"
        self.vmWriter.writePop(kind, index)
        self.parseTreeFile.write("</letStatement>\n")

    def compileWhile(self):
        self.nWhile += 1
        nWhile = self.nWhile
        self.parseTreeFile.write("<whileStatement>\n")
        self.vmWriter.writeLabel("whileStart" + str(nWhile))
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "(":
                    self.writeTerminal()
                    self.compileExpression(endTokens = [")"])
                    self.writeTerminal()
                    self.vmWriter.writeArithmetic("not")
                    self.vmWriter.writeIf("whileEnd" + str(nWhile))
                if self.tokenizer.symbol() == "{":
                    self.writeTerminal()
                    self.compileStatements()
                    self.writeTerminal()
                    self.vmWriter.writeGoto("whileStart" + str(nWhile))
                    break
            self.writeTerminal()
        self.vmWriter.writeLabel("whileEnd" + str(nWhile))
        self.parseTreeFile.write("</whileStatement>\n")

    def compileReturn(self):
        self.parseTreeFile.write("<returnStatement>\n")
        self.writeTerminal()
        if self.tokenizer.tokenType() == "SYMBOL":
            if self.tokenizer.symbol() == ";":
                self.writeTerminal()
                self.vmWriter.writePush("CONST", 0)
                self.vmWriter.writeReturn()
                self.parseTreeFile.write("</returnStatement>\n")
                return
        self.compileExpression(endTokens = [";"])
        self.vmWriter.writeReturn()
        self.writeTerminal()
        self.parseTreeFile.write("</returnStatement>\n")

    def compileIf(self):
        self.nIf += 1
        nIf = self.nIf
        elseStarted = False
        self.parseTreeFile.write("<ifStatement>\n")
        
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == "(":
                    self.writeTerminal()
                    self.compileExpression(endTokens = [")"])
                    self.writeTerminal()
                    self.vmWriter.writeArithmetic("not")
                    self.vmWriter.writeIf("elseStart" + str(nIf))
                if self.tokenizer.symbol() == "{":
                    self.writeTerminal()
                    self.compileStatements()
                    self.writeTerminal()
                    if self.tokenizer.tokenType() == "KEYWORD":
                        if self.tokenizer.symbol() == "else":
                            self.vmWriter.writeGoto("ifElseEnd" + str(nIf))
                            self.vmWriter.writeLabel("elseStart" + str(nIf))
                            elseStarted = True
                            continue
                        else:
                            if not elseStarted:
                                self.vmWriter.writeLabel("elseStart" + str(nIf))
                            break
                    else:
                        if not elseStarted:
                            self.vmWriter.writeLabel("elseStart" + str(nIf))
                        break
            self.writeTerminal()
        self.vmWriter.writeLabel("ifElseEnd" + str(nIf))
        self.parseTreeFile.write("</ifStatement>\n")

    def compileExpression(self, endTokens):
        self.parseTreeFile.write("<expression>\n")
        vmOpArray = []
        self.compileTerm()
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() in endTokens:
                    break
                elif self.tokenizer.symbol() in CompilationEngine.ops:
                    vmOp = CompilationEngine.vmOps[self.tokenizer.symbol()]
                    vmOpArray.append(vmOp)
                    self.writeTerminal()
                else:
                    self.compileTerm()
            else:
                self.compileTerm()
        for vmOp in reversed(vmOpArray):
            self.vmWriter.writeArithmetic(vmOp)
        self.parseTreeFile.write("</expression>\n")

    def compileTerm(self):
        self.parseTreeFile.write("<term>\n")
        if self.tokenizer.tokenType() == "SYMBOL":
            if self.tokenizer.symbol() in ["-", "~"]:
                unaryOp = self.tokenizer.symbol()
                self.writeTerminal()
                self.compileTerm()
                if unaryOp == "-":
                    self.vmWriter.writeArithmetic("neg")
                elif unaryOp == "~":
                    self.vmWriter.writeArithmetic("not")
            elif self.tokenizer.symbol() == "(":
                self.writeTerminal()
                self.compileExpression(endTokens = [")"])
                self.writeTerminal()
        elif self.tokenizer.tokenType() in ["KEYWORD", "STRING_CONST", "INT_CONST"]:
            # Need to deal with string cases here as well
            if self.tokenizer.tokenType() == "INT_CONST":
                self.vmWriter.writePush("CONST", self.tokenizer.intVal())
            if self.tokenizer.tokenType() == "KEYWORD":
                if self.tokenizer.keyWord() in ["false", "null"]:
                    self.vmWriter.writePush("CONST", 0)
                elif self.tokenizer.keyWord() == "true":
                    self.vmWriter.writePush("CONST", 1)
                    self.vmWriter.writeArithmetic("neg")
                elif self.tokenizer.keyWord() == "this":
                    self.vmWriter.writePush("POINTER", 0)
                else:
                    raise Exception("Should never reach here")
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
                kind = self.symbolTable.kindOf(self.tokenizer.identifier())
                index = self.symbolTable.indexOf(self.tokenizer.identifier())
                if kind == "FIELD":
                    kind = "THIS"
                self.vmWriter.writePush(kind, index)
                self.writeTerminal()
        self.parseTreeFile.write("</term>\n")

    def compileSubroutineCall(self):
        funcName = ""
        method = False
        identifier = self.tokenizer.identifier()
        varType = self.symbolTable.typeOf(identifier)
        if varType == "NONE":
            funcName += identifier
            self.writeTerminal()
        else:
            funcName += varType
            self.writeTerminal()
            method = True
        if self.tokenizer.tokenType() == "SYMBOL":
            if self.tokenizer.symbol() == ".":
                funcName += self.tokenizer.symbol()
                self.writeTerminal()
                funcName += self.tokenizer.identifier()
                self.writeTerminal()
                self.writeTerminal()
                nArgs = self.compileExpressionList(method = method, identifier=identifier)
                self.writeTerminal()
            elif self.tokenizer.symbol() == "(":
                method = True # Is this always true? Can you call a non-method func like func()?
                funcName = self.className + "." + funcName
                self.writeTerminal()
                nArgs = self.compileExpressionList(method = method, identifier=identifier)
                self.writeTerminal()
            else:
                raise Exception("Should never reach here")
        self.vmWriter.writeCall(funcName, nArgs)

    def compileExpressionList(self, method, identifier):
        self.parseTreeFile.write("<expressionList>\n")
        nArgs = 0
        if method:
            kind = self.symbolTable.kindOf(identifier)
            if kind == "FIELD":
                kind = "THIS"
                index = self.symbolTable.indexOf(identifier)
            elif kind == "NONE":
                kind = "POINTER"
                index = 0
            else:
                index = self.symbolTable.indexOf(identifier)
            self.vmWriter.writePush(kind, index)
            nArgs += 1
        while True:
            if self.tokenizer.tokenType() == "SYMBOL":
                if self.tokenizer.symbol() == ",":
                    self.writeTerminal()
                if self.tokenizer.symbol() == ")":
                    break
            self.compileExpression(endTokens = [",",")"])
            nArgs += 1
        self.parseTreeFile.write("</expressionList>\n")
        return nArgs
