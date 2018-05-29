import re
import sys
from copy import deepcopy

class Type:
    """Class defining a C++ type with optional template parameters"""
    def __init__(self, name = "", templateParams = None):
        self.name = name
        if templateParams:
            self.templateParams = templateParams
        else:
            self.templateParams = []
    def trimNames(self):
        self.name = self.name.strip()
        for x in self.templateParams:
            x.trimNames()
    def isTemplate(self):
        return len(self.templateParams) != 0
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

def parseTypeString(inTypeString):
    """Generate a Type defining the passed template type (string)"""
    curType = Type()
    curStack = []
    for c in inTypeString:
        if c == '<':
            curStack.append(curType)
            curType = Type()
            curStack[-1].templateParams.append(curType)
        elif c == '>':
            curType = curStack.pop()
        elif c == ',':
            curType = Type()
            curStack[-1].templateParams.append(curType)
        else:
            curType.name += c
    curType.trimNames()
    return curType

def cleanType(inType):
    if not inType.isTemplate():
        return inType
    inType.templateParams = [cleanType(param) for param in inType.templateParams]
    if (inType.name == "list" or inType.name == "vector") and len(inType.templateParams) == 2:
        if inType.templateParams[-1].name == "allocator" and inType.templateParams[0] == inType.templateParams[-1].templateParams[0]:
            inType.templateParams.pop()
    if inType.name == "set" and len(inType.templateParams) == 3:
        if inType.templateParams[-1].name == "allocator" and inType.templateParams[0] == inType.templateParams[-1].templateParams[0]:
            inType.templateParams.pop()
    if inType.name == "set" and len(inType.templateParams) == 2:
        if inType.templateParams[-1].name == "less" and inType.templateParams[0] == inType.templateParams[-1].templateParams[0]:
            inType.templateParams.pop()
    if inType.name == "map" and len(inType.templateParams) == 4:
        firstTypeConst = deepcopy(inType.templateParams[0])
        firstTypeConst.name += " const"
        pair = Type("pair", [firstTypeConst, inType.templateParams[1]])
        if inType.templateParams[-1].name == "allocator" and pair == inType.templateParams[-1].templateParams[0]:
            inType.templateParams.pop()
    if inType.name == "map" and len(inType.templateParams) == 3:
        if inType.templateParams[-1].name == "less" and inType.templateParams[0] == inType.templateParams[-1].templateParams[0]:
            inType.templateParams.pop()
    return inType

def cleanStd(input, stripSTD = True):
    output = re.sub(r"\b__cxx11::", "", input)
    output = re.sub(r",\s*boost::detail::variant::void_\b", "", output)
    output = re.sub(r"\bbasic_string<char(, std::char_traits<char>, std::allocator<char> )?>", "string", output)
    if stripSTD:
        output = re.sub(r"\bstd::", "", output)
    return output

def formatType(curType, indent = ""):
    """Format the passed type"""
    # When the type is not a template just return it
    if not curType.isTemplate():
        return indent + curType.name
    # Split lines of subtypes if we have template template params or the number of template params exceeds a threshold
    hasTemplateParam = any(x.isTemplate() for x in curType.templateParams)
    splitLines = hasTemplateParam or len(curType.templateParams) > 2
    
    result = indent + curType.name + "<"
    if splitLines:
        subIndent = indent + "  "
        formattedParams = [formatType(x, subIndent) for x in curType.templateParams]
        result += "\n" + ",\n".join(formattedParams)
        result += "\n" + indent + ">"
    else:
        formattedParams = [formatType(x) for x in curType.templateParams]
        result += ", ".join(formattedParams) + ">"
    return result
    

def formatTypeString(inTypeString, clean = True):
    """Format the passed type string"""
    type = parseTypeString(inTypeString)
    if clean:
        type = cleanType(type)
    formated = formatType(type)
    return formated

def findMatchingBrace(string, startPos):
    openBrace = string[startPos]
    if openBrace == "<":
        closeBrace = ">"
    elif openBrace == "(":
        closeBrace = ")"
    elif openBrace == "{":
        closeBrace = "}"
    else:
        raise "invalid brace"
    numOpen = 0
    curPos = startPos
    for c in string[startPos:]:
        if c == openBrace:
            numOpen += 1
        elif c == closeBrace:
            numOpen -= 1
            if numOpen == 0:
                return curPos
        curPos += 1
    raise "no matching brace"
    
def formatTypes(inString):
    outString = inString
    templateRE = re.compile(r"(const )?(\w|:)+(<)")
    curPos = 0
    while True:
        match = templateRE.search(inString, curPos)
        if not match:
            break
        endPos = findMatchingBrace(inString, match.start(3)) + 1
        typeStr = inString[match.start():endPos]
        formattedMatch = "\n" + formatTypeString(typeStr)
        outString = outString.replace(typeStr, formattedMatch)
        curPos = endPos
    return outString

