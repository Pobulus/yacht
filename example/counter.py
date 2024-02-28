from yacht.anchor import *

anchors = {}
_COUNTER = 0

@anchor
def get(req):
    testCookie = getCookie(req)
    print("test cookie")
    
    if "test2" in testCookie:
        print(testCookie["test2"].value)

    return str(_COUNTER)

@anchor
def increment(req):
    global _COUNTER
    _COUNTER += 1
    return str(_COUNTER)

@anchor
def decrement(req):
    global _COUNTER
    _COUNTER -= 1
    cookie = SimpleCookie()
    cookie["test"] = "increment"
    cookie["test2"] = "decrement"
    setCookie(req, cookie)
    return str(_COUNTER)