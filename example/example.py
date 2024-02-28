from datetime import datetime
import yacht.anchor as anchor



@anchor.anchor
def time(request):
    return datetime.now().strftime(anchor.getRequestBody(request).get('format', "%H:%M"))

@anchor.anchor
def printer(request): 
    print(request.headers)
    return str("clicked!")


