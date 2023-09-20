from flask import request
from services.period import findActivePeriodService, createPeriodService, updatePeriodService


def createPeriodController():
    period = {
        "year": request.json["year"],
        "start": request.json["start"],
        "active": True,
    }

    activePeriod = findActivePeriodService()

    if activePeriod is not None:
        activePeriod["active"] = False
        updatePeriodService(activePeriod)

    period = createPeriodService(period)

    return {"data": period}

def getActivePeriodController():
    activePeriod = findActivePeriodService()

    return {
        "data": activePeriod
    }