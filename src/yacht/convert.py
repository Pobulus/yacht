import sys, re, uuid, json
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

def uniqueID(prefix):
    return prefix+str(uuid.uuid4())[0:4]
    
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
    
    tugID = uniqueID("tug")
    objIterator = iter(obj)
    next(objIterator)
    filename =  obj["tug"]
    print(tugStack)
    if filename in tugStack:
        return errorElement(f"tugging {filename} from {tugStack[-1]} would cause recursion")    
    tugStack.append(filename)
    try:
        file = loadFile(filename)

        token = next(objIterator, None)
        while token is not None:
            file = file.replace(f"${token}", obj[token])
            token = next(objIterator, None)
        file = re.sub(r"id: *('?)(\w+)", fr"id: \1{tugID}_\2", file)
        
        output = parseFile(file, indent+indentSpaces, tugStack)
    except FileNotFoundError:
        tugStack.pop()
        return errorElement(f"file {obj['tug']} was not found")
    tugStack.pop()
    return output

def parseAnchor(obj, indent, id):
    output = ""
    if obj is not None:
        for anchor in obj:
            arguments = json.dumps(anchor.get('arguments', None))
            target = anchor.get('target', "")
            trigger = anchor.get('trigger', "")
            output += f"\n{' '*indent}<script>harbour.bindAnchor(\"{id}\", \"{anchor['bind']}\", {arguments}, \"{target}\", \"{trigger}\");</script>"
    return output
def parseHTMLObj(obj, indent, tugStack=[]):
    output = ""
    objIterator = iter(obj)
    tag = next(objIterator) # get first key as tag name
    content = obj[tag]
    if(tag == "craft"):
        return craftHTML(obj, indent)
    elif(tag == "tug"):
        return tugFile(obj, indent, tugStack)
    elif(tag=="script"):
        if(type(content) == str and not '\n' in content):
            return f"\n{' '*indent}<script src=\"{content}\"></script>"
    elif(tag=="style"):
        if(type(content) == str and not '\n' in content):
            return f"\n{' '*indent}<link rel=\"stylesheet\" href=\"{content}\" />"
    output += f"\n{' '*indent}<{tag}"
    # following keys as attributes
    attributes = []
    anchors = None
    anchorsID = ""
    if "anchors" in obj.keys():
            anchors = obj['anchors']
            anchorsID = obj.get("id", uniqueID("anchor"))
            obj["id"] = anchorsID
            objIterator = iter(obj) # recreate the iterator after modifying obj
            next(objIterator) # skip first key
            

    attrTemp = next(objIterator, None)

    while attrTemp is not None and attrTemp != "anchors":
        output += f" {attrTemp}=\"{obj[attrTemp]}\""
        attrTemp = next(objIterator, None)
    if tag in emptyElementTags:
        output += " />"
        output += parseAnchor(anchors, indent, anchorsID)
        return output;
    
    output += ">"
    
    if content is None:
        output += f"</{tag}>"
        output += parseAnchor(anchors, indent, anchorsID)
        return output
    else:
        if(type(content)==str):  
            if '\n' in content:
                if (tag != "script"):
                    content = content.replace('\n', '<br />\n')
                output += f"\n{content}\n{' '*indent}</{tag}>"
            else:
                output += f"{content}</{tag}>"
            output += parseAnchor(anchors, indent, anchorsID)
            return output
        elif(tag == "style"):
            for child in content:
                output += f"{parseCSSObj(child, indent+indentSpaces)}"
            
        else: 
            for child in content:
                output += f"{' '*indent}{parseHTMLObj(child, indent+indentSpaces, tugStack)}"
    output += f"\n{' '*indent}</{tag}>"
    output += parseAnchor(anchors, indent, anchorsID)
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

def loadFile(filename):
    print(f"loading file {filename}")
    with open(filename, 'rt', encoding='utf8') as file:
        return file.read()
    





def parseFile(file, indent=0, tugStack=[]):
    output = ""
    
    data = load(file, Loader=Loader)
    root = next(iter(data))
     
    if len(tugStack) <  2:
        
        if(root == "html"):
            output += "<!DOCTYPE html>\n"
            output += "<!--  Created using YACHT -->\n"
            output += "<!-- Have a very nice day! -->\n"
            output += parseHTMLObj(data, indent, tugStack)
        elif(root == "style"):
            output += "/*  Created using YACHT */\n"
            output += "/* Have a very nice day! */\n"
            for child in data["style"]:
                output += f"{parseCSSObj(child, indent)}"
        
    elif(root == "html"):
        return errorElement("tugged pages cannot start with html")
    else:
        output += parseHTMLObj(data, indent, tugStack)
    
    return output;

def convertFile(filename, indent=0):
    file = loadFile(filename)
    return parseFile(file, 0, [filename])


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv)>1 else "input.yaml" 
    print(convertFile(filename))
    