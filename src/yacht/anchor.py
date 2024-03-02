import functools, json, sys
from http.cookies import SimpleCookie


anchorsJS = """
var harbour=void 0;class Anchor{constructor(e,t,s,r){this.element=e,this.name=t,this.args=s,this.target=r}updateTarget(e){e&&("href"===this.target?window.location.href=e:"redirect"===this.target&&window.location.replace(e)),this.target&&(this.element[this.target]=e)}compareArgs(e){return!this.args||Object.keys(this.args).filter(t=>e[t]&&e[t]===this.args[t]).length===Object.keys(this.args).length}send(){let e=new XMLHttpRequest;e.open("POST",`http://${window.location.host}/anchor/${this.name}`),e.send(JSON.stringify({value:this.element.value,arguments:this.args})),e.responseType="text",e.onload=()=>{4==e.readyState&&200==e.status?(this.updateTarget(e.responseText),this.name in harbour.chainedAnchors&&harbour.chainedAnchors[this.name].forEach(t=>{t.compareArgs(this.args)&&t.updateTarget(e.responseText)})):(console.log(`Error: ${e.status}`),console.log(`happended on anchor: ${this}`))}}}class Harbour{anchors=[];pollingTargets=[];chainedAnchors={};pollingDelay=500;pollingInterval=null;bindAnchor(e,t,s,r,n){let a=new Anchor(document.getElementById(e),t,s,r);if(this.anchors.push(a),"always"===n?this.pollingTargets.push(a):"chain"===n&&(t in this.chainedAnchors||(this.chainedAnchors[t]=[]),this.chainedAnchors[t].push(a)),n){if("once"===n||"always"===n)a.send();else{let h=document.getElementById(e)[n];document.getElementById(e)[n]=function(){h&&h(),a.send()}}}}request(e){harbour.pollingTargets.forEach(e=>{e.send()})}startPolling(){clearInterval(this.pollingInterval),this.pollingInterval=setInterval(function(){harbour.request()},this.pollingDelay)}}harbour=new Harbour,document.addEventListener("DOMContentLoaded",function(e){harbour.startPolling()});
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
    