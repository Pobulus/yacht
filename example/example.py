from datetime import datetime
from yacht.anchor import *
import random

@anchor
def time(request):
    return datetime.now().strftime(anchor.getRequestBody(request).get('format', "%H:%M"))

@anchor
def printer(request): 
    print(getRequestBody(request).get("attributes", {}))
    return str("clicked!")

splashes = [
    "Land ahoy!",
    "Drop the anchor!",
    "Set sail!",
    "All aboard!"
]

@anchor
def splash(req):
    return(random.sample(splashes, 1)[0])

