import re
import sys

def cleanStd(input, stripSTD = True):
    output = re.sub(r"\b__cxx11::", "", input)
    output = re.sub(r",\s*boost::detail::variant::void_\b", "", output)
    output = re.sub(r"\bbasic_string<char>", "string", output)
    if stripSTD:
        output = re.sub(r"\bstd::", "", output)
    return output

def generateTemplateDef(inType):
    cur = ""
    curDepth = 0
    result = list()
    curList = result
    curStack = [result]
    for c in inType:
        if c == '<':
            curStack.append(curList)
            curList = []
            curStack[-1].append(curList)
            curList.append(cur.strip() + c)
            cur = ""
        elif c == '>':
            cur = cur.strip()
            if cur:
                curList.append(cur)
            curList.append(c)
            cur = ""
            curList = curStack.pop()
        elif c == ',':
            curList.append(cur.strip() + c)
            cur = ""
        else:
            cur += c
    if len(cur) > 0:
        curList.append(cur.strip())
    return result

def printTemplate(templateDef, indent = ""):
    hasTemplateInside = any(type(x) is list for x in templateDef)
    splitLines = hasTemplateInside or len(templateDef) > 4
    subIndent = indent + "  " if splitLines else ""
    templateDef[1:-1] = [subIndent + x if type(x) is str else x for x in templateDef[1:-1]]
    templateDef = [x if type(x) is str else printTemplate(x, subIndent) for x in templateDef]
    if splitLines:
        templateDef[0] = indent + templateDef[0]
        templateDef[-1] = indent + templateDef[-1]
        result = "\n".join(templateDef)
    else:
        templateDef = [x + " " if x[-1] == "," else x for x in templateDef]
        result = indent + "".join(templateDef)
    return result
    

def formatTemplate(inType):
    templateDef = generateTemplateDef(inType)
    formated = printTemplate(templateDef[0])
    formated = re.sub(r">\n\s*,", ">,", formated)
    templateDef[0] = formated
    return " ".join(templateDef)

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
        formattedMatch = "\n" + formatTemplate(typeStr)
        outString = outString.replace(typeStr, formattedMatch)
        curPos = endPos
    return outString

