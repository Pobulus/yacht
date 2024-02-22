import sys, re, ast
try:
    from yaml import load
except ImportError:
    raise RuntimeError("Looks like you haven't installed PyYAML yet")
   
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

indentSpaces = 4
eval_enabled = False

def evaluateExpression(expression):
    try:
        return str(eval(expression.group(1))) 
    except (SyntaxError, TypeError):
        return expression.group(0)
    
def generateHTML(obj, indent):

    repeat = obj.get("repeat", 1)
    
    index = obj.get("index", "$index")
   
    output = ""
    for i in range(repeat):
        for child in obj["generate"]:
            output += f"{' '*indent}{parseHTMLObj(child, indent+indentSpaces)}".replace(index, str(i))
    name = obj.get("name")
    if name is not None:
        output = f"\n{' '*indent}<-- { name or 'generated segment' } -->${output}\n{' '*indent}<-- end of {name or 'generated segment' } -->"
    return output


def parseHTMLObj(obj, indent):
    output = ""
    objIterator = iter(obj)
    tag = next(objIterator) # get first key as tag name
    if(tag == "generate"):
        return generateHTML(obj, indent)
    output += f"\n{' '*indent}<{tag}"
    # following keys as attributes
    attributes = []
    attrTemp = next(objIterator, None)
    while attrTemp is not None:
        output += f" {attrTemp}=\"{obj[attrTemp]}\""
        attrTemp = next(objIterator, None)

    output += ">"
    content = obj[tag]
    if content is None:
        output += f"</{tag}>"
        return output
    else:
        if(type(content)==str):  
            if '\n' in content:
                if (tag != "script"):
                    content = content.replace('\n', '<br />\n')
                output += f"\n{content}\n{' '*indent}</{tag}>"
            else:
                output += f"{content}</{tag}>"
            return output
        elif(tag == "style"):
            for child in content:
                output += f"{parseCSSObj(child, indent+indentSpaces)}"
            
        else: 
            for child in content:
                output += f"{' '*indent}{parseHTMLObj(child, indent+indentSpaces)}"
    output += f"\n{' '*indent}</{tag}>"
    return output

def parseCSSRule(obj, indent):
    output = ""
    objIterator = iter(obj)
    rule = next(objIterator) # get first key as tag name
    output += f"\n{' '*indent}{rule} {'{'}"
    selectors = obj[rule]
    if selectors is not None:
        for selector in selectors:
            output += f"{parseCSSObj(selector, indent+indentSpaces)}"
    output += f"\n{' '*indent}{'}'}"
    return output

def parseCSSObj(obj, indent):
    output = ""
    objIterator = iter(obj)
    selector = next(objIterator) # get first key as tag name
    if selector[0]=="@":
        return parseCSSRule(obj, indent)
    output += f"\n{' '*indent}{selector} {'{'}"
    content = obj[selector]
    if content is None:
        output += "}"
        return output
    else:
        if(type(content)==str):  
            if '\n' in content:
                output += f"\n{content}\n{' '*indent}{'}'}"
            else:
                output += f" {content} {'}'}"
            return output
        else: 
            output += "\n"
            for child in content:
                key = next(iter(child))
                output += f"{' '*(indent+indentSpaces)}{key}: {child[key]};\n"
    output += f"{' '*indent}{'}'}"
    return output


def convertFile(filename):
    output = ""
    with open(filename, 'rt', encoding='utf8') as file:
        data = load(file, Loader=Loader)

        if(next(iter(data))=="html"):
            output += "<!DOCTYPE html>\n"
        output += "<!--  Created using YACHT -->\n"
        output += "<!-- Have a very nice day! -->\n"
        output += parseHTMLObj(data, 0)
        if(eval_enabled):
            output = re.sub(r"(?:\${)(.+?)(?<!\\)(?:}\$)",evaluateExpression, output)
        
    return output;


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv)>1 else "input.yaml" 
    convertFile(filename)
    