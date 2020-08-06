class JackTokenizer:
    def __init__(self, file):
        self.file = file
        self.lines = file.readlines()
        self.totalLineNum = len(self.lines)
        self.lineNum = -1