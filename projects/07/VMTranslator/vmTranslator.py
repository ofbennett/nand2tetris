import sys
from os import path
from parser import Parser
from codeWriter import CodeWriter

filePath = sys.argv[1]
fullPath = path.abspath(filePath)
fileName = path.basename(filePath)
pathToDir = path.dirname(fullPath)

sourceFile = open(fullPath, "r")
asmFile = open(pathToDir + "/" + fileName.split(".")[0] + ".asm", "w")

parser = Parser()
codeWriter = CodeWriter(asmFile, fileName.split(".")[0])

for line in sourceFile:
    line = parser.removeComments(line)
    if line == "":
        continue
    command = line
    comType = parser.commandType(command)
    if comType == "C_ARITHMETIC":
        codeWriter.writeArithmetic(command)
    elif comType in ["C_PUSH", "C_POP"]:
        pushPop = parser.arg0(command)
        segment = parser.arg1(command)
        index = parser.arg2(command)
        codeWriter.writePushPop(pushPop, segment, index)

sourceFile.close()
asmFile.close()