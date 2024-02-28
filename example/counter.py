from yacht.anchor import *

anchors = {}
_COUNTER = 0

@anchor
def get(req):
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
    return str(_COUNTER)