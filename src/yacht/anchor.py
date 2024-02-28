import functools, json, sys
from http.cookies import SimpleCookie


anchorJS = """
class Anchor{constructor(element,name,args,target){this.element=element;this.name=name;this.args=args;this.target=target;this.redirect=undefined;}addRedirect(href){this.redirect=href;}send(){constxhr=newXMLHttpRequest();xhr.open("POST",`http://${window.location.host}/anchor/${this.name}`);xhr.send(JSON.stringify({value:this.element.value,arguments:this.args}));xhr.responseType="text";xhr.onload=()=>{if(xhr.readyState==4&&xhr.status==200){if(xhr.responseText){if(this.target==='href'){window.location.href=xhr.responseText;}else{if(this.target==='redirect'){window.location.replace(xhr.responseText);}}}if(this.target){this.element[this.target]=xhr.responseText;}}else{console.log(`Error:${xhr.status}`);console.log(`happendedonanchor:${this}`);}};}}class Anchors{anchors=[];pollingTargets=[];pollingDelay=500;pollingInterval=null;bindAnchor(id,name,args,target,trigger,redirect){constanchor=newAnchor(document.getElementById(id),name,args,target);this.anchors.push(anchor);if(trigger==='always'){this.pollingTargets.push(anchor);}if(redirect){anchor.addRedirect(redirect);}if(trigger){if(trigger==='once'||trigger==='always'){anchor.send();}else{constpreviousFunction=document.getElementById(id)[trigger];document.getElementById(id)[trigger]=function(){if(previousFunction)previousFunction();anchor.send();}}}}request(harb){harbour.pollingTargets.forEach(anchor=>{anchor.send();});}startPolling(){clearInterval(this.pollingInterval);this.pollingInterval=setInterval(function(){harbour.request();},this.pollingDelay);}}varharbour=undefined;(function(){harbour=newAnchors();document.addEventListener("DOMContentLoaded",function(event){harbour.startPolling();});}())
"""
_anchorModules = {}

def getRequestBody(request):
    reqLength = int(request.headers.get('content-length', 0))
    reqBody = request.rfile.read(reqLength).decode('UTF-8')
    obj = json.loads(reqBody)
    return obj if obj else {}
    
def getCookie(request):
    return SimpleCookie(request.headers.get('Cookie'))

def setCookie(request, cookie):
    for morsel in cookie.values():
        request.send_header("Set-Cookie", morsel.OutputString())

def anchor(func):
    @functools.wraps(func)
    def auto_func(req):
        return func(req)
    global _anchorModules
    moduleName = func.__globals__['__file__'].split('/')[-1][:-3]
    
    if not moduleName in _anchorModules.keys():
        _anchorModules[moduleName] = {}
    _anchorModules[moduleName][func.__name__] = auto_func
    return auto_func

if __name__ == "__main__":
    helpMessage = """
        This module shouldn't be run

        import it into your module like:

        from yacht.anchor import *

        then use @anchor before any function to make it accessible from yacht generated pages
        place your module .py scirpt in the root directory of your page and import it when launching yacht sail 
        by passing it's name in the list after -m 
    """
    print(helpMessage)
    