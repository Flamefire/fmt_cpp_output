import re

class terminalColors:
    LRed = '\033[91m'
    LGreen = '\033[92m'
    LYellow = '\033[93m'
    LBlue = '\033[94m'
    LMagenta = '\033[95m'
    End = '\033[0m'
    Bold = '\033[1m'
    Underline = '\033[4m'

def colorFilenames(inString):
    def makeColoredFilename(match):
        return terminalColors.LYellow + terminalColors.Bold + match.group() + terminalColors.End
    def makeColoredError(match):
        fullMatch = match.group()
        return fullMatch.replace(match.group(3), terminalColors.LRed + terminalColors.Bold + match.group(3) + terminalColors.End)
    reFilename = r"^(\w|/|\.)+:(\d+:){0,2} "
    inString = re.sub(reFilename + r"(error: .*?)$", makeColoredError, inString, flags = re.MULTILINE)
    inString = re.sub(reFilename, makeColoredFilename, inString, flags = re.MULTILINE)
    return inString
