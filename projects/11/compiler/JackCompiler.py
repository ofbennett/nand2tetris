import sys
from os import path, mkdir
from glob import glob
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

debugDirName = "debugXMLFiles"

dirPath = sys.argv[1]
sourceFiles = glob(dirPath+"*.jack")
sourceFilesFullPath = [path.abspath(f) for f in sourceFiles]

debugDir = dirPath + debugDirName + "/"
if not path.isdir(debugDir):
    mkdir(debugDir)

for f in sourceFilesFullPath:
    fileName = path.basename(f)
    sourceFile = open(f, "r")
    tokXMLFile = open(debugDir + fileName.split(".")[0] + "T.xml", "w")
    parseTreeXMLFile = open(debugDir + fileName.split(".")[0] + ".xml", "w")
    comp = CompilationEngine(sourceFile, tokXMLFile, parseTreeXMLFile)
    comp.compileClass()

    sourceFile.close()
    tokXMLFile.close()
    parseTreeXMLFile.close()
