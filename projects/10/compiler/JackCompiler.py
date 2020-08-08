import sys
from os import path, mkdir
from glob import glob
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

resultDirName = "intermediateFiles"

tokTypeDict = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier", "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}

dirPath = sys.argv[1]
baseName = path.basename(dirPath[:-1])
sourceFiles = glob(dirPath+"*.jack")
sourceFilesFullPath = [path.abspath(f) for f in sourceFiles]

resultDir = dirPath + resultDirName + "/"
if not path.isdir(resultDir):
    mkdir(resultDir)

# Produce tokenized ...T.xml files
for f in sourceFilesFullPath:
    fileName = path.basename(f)
    sourceFile = open(f, "r")
    tokFile = open(resultDir + fileName.split(".")[0] + "T.xml", "w")
    tokenizer = JackTokenizer(sourceFile)
    tokFile.write("<tokens>\n")
    while tokenizer.hasMoreTokens():
        tokType = tokenizer.tokenType()
        tokFile.write(f"<{tokTypeDict[tokType]}> ")
        if tokType == "KEYWORD":
            tok = tokenizer.keyWord()
        elif tokType == "SYMBOL":
            tok = tokenizer.symbol()
        elif tokType == "IDENTIFIER":
            tok = tokenizer.identifier()
        elif tokType == "INT_CONST":
            tok = tokenizer.intVal()
        elif tokType == "STRING_CONST":
            tok = tokenizer.stringVal()
        tokFile.write(tok)
        tokFile.write(f" </{tokTypeDict[tokType]}>\n")
        tokenizer.advance()

    tokFile.write("</tokens>")
    sourceFile.close()
    tokFile.close()

# Produce parsed .xml files
for f in sourceFilesFullPath:
    fileName = path.basename(f)
    sourceFile = open(f, "r")
    parsedFile = open(resultDir + fileName.split(".")[0] + ".xml", "w")
    tokenizer = JackTokenizer(sourceFile)
    comp = CompilationEngine()

    sourceFile.close()
    parsedFile.close()
