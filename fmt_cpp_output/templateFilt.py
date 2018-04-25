import re
import sys

class Type:
    """Class defining a C++ type with optional template parameters"""
    def __init__(self):
        self.name = ""
        self.templateParams = []
    def trimNames(self):
        self.name = self.name.strip()
        for x in self.templateParams:
            x.trimNames()
    def isTemplate(self):
        return len(self.templateParams) != 0

def cleanStd(input, stripSTD = True):
    output = re.sub(r"\b__cxx11::", "", input)
    output = re.sub(r",\s*boost::detail::variant::void_\b", "", output)
    output = re.sub(r"\bbasic_string<char(, std::char_traits<char>, std::allocator<char> )?>", "string", output)
    output = re.sub(r"\b(list<(.*)), std::allocator<\2> >", r"\1>", output)
    output = re.sub(r"\b(set<(.*?)), std::less<\2>, std::allocator<\2> >", r"\1>", output)
    output = re.sub(r"\b(map<(.*?), (.*?)), std::less<\2>, std::allocator<std::pair<\2 const, \3> >", r"\1>", output)
    if stripSTD:
        output = re.sub(r"\bstd::", "", output)
    return output

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

def formatType(curType, indent = ""):
    """Formats the passed type"""
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
    

def formatTypeString(inTypeString):
    """Formats the passed type string"""
    type = parseTypeString(inTypeString)
    formated = formatType(type)
    #formated = re.sub(r">\n\s*,", ">,", formated)
    #templateDef[0] = formated
    #return " ".join(templateDef)
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

