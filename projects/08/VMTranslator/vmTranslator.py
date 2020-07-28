import sys
from os import path
from glob import glob
from parser import Parser
from codeWriter import CodeWriter

filePath = sys.argv[1]
baseName = path.basename(filePath[:-1])
sourceFiles = glob(filePath+"*.vm")
sourceFilesFullPath = [path.abspath(f) for f in sourceFiles]
asmFile = open(filePath + baseName + ".asm", "w")
parser = Parser()
codeWriter = CodeWriter(asmFile)
codeWriter.writeInit()

for f in sourceFilesFullPath:
    fileName = path.basename(f)
    codeWriter.fileName = fileName
    sourceFile = open(f, "r")
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
        elif comType == "C_LABEL":
            label = parser.arg1(command)
            codeWriter.writeLabel(label)
        elif comType == "C_GOTO":
            label = parser.arg1(command)
            codeWriter.writeGoto(label)
        elif comType == "C_IF":
            label = parser.arg1(command)
            codeWriter.writeIf(label)
        elif comType == "C_FUNCTION":
            funcName = parser.arg1(command)
            numLocals = parser.arg2(command)
            codeWriter.writeFunction(funcName, numLocals)
        elif comType == "C_RETURN":
            codeWriter.writeReturn()
        elif comType == "C_CALL":
            funcName = parser.arg1(command)
            numArgs = parser.arg2(command)
            codeWriter.writeCall(funcName, numArgs)
    sourceFile.close()

asmFile.close()