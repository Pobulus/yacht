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
__uniqueTugCounter = 0
eval_enabled = False

emptyElementTags = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr"
]

    
def craftHTML(obj, indent):

    repeat = obj.get("repeat", 1)
    
    index = obj.get("index", "$index")
   
    output = ""
    for i in range(repeat):
        for child in obj["craft"]:
            output += f"{' '*indent}{parseHTMLObj(child, indent+indentSpaces)}".replace(index, str(i))
    name = obj.get("name")
    if name is not None:
        output = f"\n{' '*indent}<-- { name or 'crafted segment' } -->${output}\n{' '*indent}<-- end of {name or 'crafted segment' } -->"
    return output

def tugFile(obj, indent, tugStack):
    global __uniqueTugCounter
    objIterator = iter(obj)
    next(objIterator)
    try:
        output = convertFile(obj["tug"], indent+indentSpaces, tugStack)
    except FileNotFoundError:
        return errorElement(f"file {obj[tag]} was not found")
    token = next(objIterator, None)
    while token is not None:
        output = output.replace(f"${token}", obj[token])
        token = next(objIterator, None)
    output = output.replace(f" id=\"", f" id=\"tug{__uniqueTugCounter}_")
    output = re.sub(r"#(.+) {", fr"#tug{__uniqueTugCounter}_\1 {{", output)
    __uniqueTugCounter += 1
    return output

def parseHTMLObj(obj, indent, tugStack=[]):
    output = ""
    objIterator = iter(obj)
    tag = next(objIterator) # get first key as tag name
    if(tag == "craft"):
        return craftHTML(obj, indent)
    elif(tag == "tug"):
        return tugFile(obj, indent, tugStack)
    output += f"\n{' '*indent}<{tag}"
    # following keys as attributes
    attributes = []
    attrTemp = next(objIterator, None)
    while attrTemp is not None:
        output += f" {attrTemp}=\"{obj[attrTemp]}\""
        attrTemp = next(objIterator, None)
    if tag in emptyElementTags:
        output += " />"
        return output;

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
                output += f"{' '*indent}{parseHTMLObj(child, indent+indentSpaces, tugStack)}"
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

def errorElement(message):
    return f"<b style=\"color:red\">Error:{message}</b>"

def convertFile(filename, indent=0, tugStack=[]):
    output = ""
    print(f"converting file {filename}")
    with open(filename, 'rt', encoding='utf8') as file:
        data = load(file, Loader=Loader)
        root = next(iter(data))
        
        if filename in tugStack:
            return errorElement(f"tugging {filename} from {tugStack[-1]} would cause recursion")
        
        if not tugStack:
            uniqueCounter = 0
            if(root == "html"):
                output += "<!DOCTYPE html>\n"
                output += "<!--  Created using YACHT -->\n"
                output += "<!-- Have a very nice day! -->\n"
                tugStack.append(filename)
                output += parseHTMLObj(data, indent, tugStack)
            elif(root == "style" and not len(tugStack)):
                output += "/*  Created using YACHT */\n"
                output += "/* Have a very nice day! */\n"
                tugStack.append(filename)
                for child in data["style"]:
                    output += f"{parseCSSObj(child, indent)}"
            
        elif(root == "html"):
            return errorElement("tugged pages cannot start with html")
        else:
            tugStack.append(filename)
            output += parseHTMLObj(data, indent, tugStack)
        tugStack.pop()    
    return output;


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv)>1 else "input.yaml" 
    print(convertFile(filename))
    