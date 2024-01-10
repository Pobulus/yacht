from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

indentSpaces = 4

def parseHTMLObj(obj, indent):
    output = ""
    objIterator = iter(obj)
    tag = next(objIterator) # get first key as tag name
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

def parseCSSObj(obj, indent):
    output = ""
    objIterator = iter(obj)
    selector = next(objIterator) # get first key as tag name
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


with open("input.yaml", 'r') as file:
    data = load(file, Loader=Loader)

    if(next(iter(data))=="html"):
        print("<!DOCTYPE html>")
    print("<!--  Created using YACHT -->")
    print("<!-- Have a very nice day! -->")
    print(parseHTMLObj(data, 0))

