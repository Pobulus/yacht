from datetime import datetime
import anchor 



@anchor._anchor
def time(request):
    return datetime.now().strftime(anchor.getRequestBody(request).get('format', "%H:%M"))

@anchor._anchor
def printer(request): 
    print(request.headers)
    return str("clicked!")
# anchors = {
#     "time": time, 
#     "print":printer
# }

