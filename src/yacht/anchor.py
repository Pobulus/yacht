import functools, json, sys
from http.cookies import SimpleCookie

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
    