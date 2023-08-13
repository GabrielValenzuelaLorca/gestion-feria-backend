from flask import request
from services.period import findActiveService, createService, updateService


def createController():
    period = {
        "year": request.json["year"],
        "start": request.json["start"],
        "active": True,
    }

    activePeriod = findActiveService()

    if activePeriod is not None:
        activePeriod["active"] = False
        updateService(activePeriod)

    period = createService(period)

    return {"data": period}
