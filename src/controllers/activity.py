from flask import request
from flask_api import status
from services.activity import (
    editActivityService,
    getActivityService,
    getAppActivitiesService,
    newActivityService,
    getActivitiesService,
)
from services.period import findActivePeriodService


def newActivityController():
    activity = request.json
    activePeriod = findActivePeriodService()

    if activePeriod is None:
        return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR

    activity["period"] = activePeriod["id"]
    activity["rubric"] = None
    activity = newActivityService(activity)

    return {"data": activity}


def editActivityController():
    activity = request.json
    activity = editActivityService(activity)

    return {"data": activity}


def getActivitiesController():
    activities = getActivitiesService()

    activities.sort(key=lambda x: x["end"], reverse=True)

    return {"data": activities}


def getActivityController(activity_id):
    activity = getActivityService(activity_id)

    return {"data": activity}


def getAppActivitiesController():
    activities = getAppActivitiesService()

    return {"data": activities}
