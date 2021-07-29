from app import db
from app.models import Implant, Caps, RestorativeParts

def getImplants():
    allImplants = []

    implantQuery = Implant.query.all()

    # OrderBy might be expensive, see about adding in sorted order
    for i in implantQuery:
        allImplants.append((i.id, i.data))

    return allImplants


def getCaps():
    allCaps = []

    for c in Caps.query.order_by(Caps.data):
        allCaps.append((c.id, c.data))

    return allCaps


def getParts():
    allParts = []

    for p in RestorativeParts.query.order_by(RestorativeParts.data):
        allParts.append((p.id, p.data))

    return allParts