from collections import deque

class JackTokenizer:
    def __init__(self, file):
        self.file = file
        self.decommentedCode = ""
        self.tokenQueue = deque()
        self._removeComments()
        self._tokenizeLines()

    def _removeComments(self):
        withinComment = False
        for line in self.file.readlines():
            if withinComment:
                line = line.strip()
                if len(line) > 1:
                    if line[-2:] == "*/":
                        withinComment = False
                        continue
                continue

            line = line.split("//")[0].strip()
            commentSplit = line.split("/*")
            line = commentSplit[0].strip()
            if len(commentSplit) > 1:
                withinComment = True
                comment = commentSplit[1].strip()
                if len(comment) > 1:
                    if comment[-2:] == "*/":
                        withinComment = False
            if len(line) == 0:
                continue
            self.decommentedCode += line
        self.file.seek(0)

    def _tokenizeLines(self):
        symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
        allowedLetters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_"}
        code = self.decommentedCode

        start = 0
        end = 1
        inString = False
        inKWorID = False # In keyword or identifier
        reset = True
        while end < len(code)+1:
            if reset:
                if code[start:end] in symbols:
                    self.tokenQueue.append(code[start:end])
                    start = end
                    end +=1
                    reset = True
                elif code[start:end] == ' ':
                    start = end
                    end +=1
                    reset = True
                elif code[start:end] == '"':
                    inString = True
                    reset = False
                elif code[start:end] in allowedLetters:
                    inKWorID = True
                    reset = False
                else:
                    raise Exception(f"Unrecognized symbol encountered: {code[start:end]}")
            else:
                if inString:
                    end += 1
                    while code[end-1] != '"':
                        end += 1
                elif inKWorID:
                    while code[end] in allowedLetters:
                        end += 1
                else:
                    raise Exception(f"Neither in String, Keyword or Identifier")
                self.tokenQueue.append(code[start:end])
                start = end
                end +=1
                inString = False
                inKWorID = False
                reset = True


    def hasMoreTokens(self):
        return len(self.tokenQueue) > 0

    def advance(self):
        self.tokenQueue.popleft()

    def tokenType(self):
        keywords = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
        symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
        numbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}
        tok = self.tokenQueue[0]
        if tok in symbols:
            return "SYMBOL"
        elif tok in keywords:
            return "KEYWORD"
        elif tok[0] == '"':
            return "STRING_CONST"
        elif tok[0] in numbers:
            return "INT_CONST"
        else:
            return "IDENTIFIER"

    def keyWord(self):
        return self.tokenQueue[0]

    def symbol(self):
        symbolDict = {"<": "&lt;",">": "&gt;","&": "&amp;"}
        tok = self.tokenQueue[0]
        if tok in symbolDict.keys():
            tok = symbolDict[tok]
        return tok

    def identifier(self):
        return self.tokenQueue[0]

    def intVal(self):
        return self.tokenQueue[0]

    def stringVal(self):
        return self.tokenQueue[0][1:-1]
    
    def lookAheadOne(self):
        return self.tokenQueue[1]