import functools, json


def getRequestBody(request):
    reqLength = int(request.headers.get('content-length', 0))
    reqBody = request.rfile.read(reqLength).decode('UTF-8')
    obj = json.loads(reqBody)
    return obj if obj else {}
    

def _anchor(func, name=""):
    @functools.wraps(func)
    def auto_func(req):
        func(req)
    if not name:
        name = func.__name__
    anchors[name] = auto_func
    return func

