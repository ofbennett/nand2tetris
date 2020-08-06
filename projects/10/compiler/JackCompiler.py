import sys
from os import path, mkdir
from glob import glob
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

resultDirName = "intermediateFiles"

dirPath = sys.argv[1]
baseName = path.basename(dirPath[:-1])
sourceFiles = glob(dirPath+"*.jack")
sourceFilesFullPath = [path.abspath(f) for f in sourceFiles]

resultDir = dirPath + resultDirName + "/"
if not path.isdir(resultDir):
    mkdir(resultDir)


# comp = CompilationEngine()

for f in sourceFilesFullPath:
    fileName = path.basename(f)
    sourceFile = open(f, "r")
    tokFile = open(resultDir + fileName.split(".")[0] + "T.xml", "w")

    tok = JackTokenizer(sourceFile) 

    sourceFile.close()
    tokFile.close()
