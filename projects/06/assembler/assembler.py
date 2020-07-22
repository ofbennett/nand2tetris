import sys
from code import Code
from parser import Parser
from os import path

filePath = sys.argv[1]
fullPath = path.abspath(filePath)
sourceFile = open(fullPath, "r")
fileName = path.basename(filePath)
hackFile = open(fileName.split(".")[0] + ".hack", "w")

parser = Parser(sourceFile)
code = Code()

parser.removeCommentsAndWhiteSpace()

while parser.hasMoreCommands():
    parser.advance()
    commandType = parser.commandType()
    if commandType == "L_COMMAND":
        symbol = parser.symbol()
        # Add label to symbol table

    elif commandType == "A_COMMAND":
        symbol = parser.symbol()
        if symbol.isnumeric():
            address = "{0:015b}".format(int(symbol))
        else:
            pass # Use symbol table
        aCode = "0" + address
        hackFile.write(aCode)
        hackFile.write("\n")

    elif commandType == "C_COMMAND":
        dest = parser.dest()
        comp = parser.comp()
        jump = parser.jump()
        cCode = "111" + code.comp(comp) + code.dest(dest) + code.jump(jump)
        hackFile.write(cCode)
        hackFile.write("\n")

sourceFile.close()
hackFile.close()

# print(parser.commandsWithLables)