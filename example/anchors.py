from datetime import datetime
import json

def getRequestBody(request):
    reqLength = int(request.headers.get('content-length', 0))
    reqBody = request.rfile.read(reqLength).decode('UTF-8')
    obj = json.loads(reqBody)
    return obj if obj else {}
    


def time(request):
    return datetime.now().strftime(getRequestBody(request).get('format', "%H:%M"))
def printer(request): 
    print(getRequestBody(request).get('format', "%H:%M"))
    return ""
anchors = {
    "time": time, 
    "print":printer
}

