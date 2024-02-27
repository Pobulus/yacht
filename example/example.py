from datetime import datetime




def time(request):
    return datetime.now().strftime(getRequestBody(request).get('format', "%H:%M"))
def printer(request): 
    print(getRequestBody(request).get('format', "%H:%M"))
    return ""
anchors = {
    "time": time, 
    "print":printer
}

