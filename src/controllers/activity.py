from datetime import datetime
from pytz import timezone
from flask import g, request
from flask_api import status
from services.activity import (
    editActivityService,
    getActivityService,
    getAppActivitiesService,
    newActivityService,
    getActivitiesService,
)
from services.deliverable import (
    getDeliverablesByActivityService,
    getDeliverablesByTeamService,
    updateDeliverablesService,
)
from services.period import findActivePeriodService


def newActivityController():
    activity = request.json
    activePeriod = findActivePeriodService()

    if activePeriod is None:
        return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR

    activity["close"] = activity["close"] if activity["close"] != "" else None
    activity["period"] = activePeriod["id"]
    activity["rubric"] = None
    activity = newActivityService(activity)

    return {"data": activity}


def editActivityController():
    activity = request.json
    activity = editActivityService(activity)

    updateDeliverablesService({"activity.id": activity["id"]}, {"activity": activity})

    return {"data": activity}


def getActivitiesController():
    activities = getActivitiesService()

    activities.sort(key=lambda x: x["end"], reverse=True)

    return {"data": activities}


def getActivityController(activity_id):
    activity = getActivityService(activity_id)

    return {"data": activity}


def getAppActivitiesController():
    tz = timezone("America/Santiago")
    currentDate = datetime.now(tz)

    def getDateTime(date, time="T23:59"):
        return tz.localize(datetime.strptime(date + time, "%Y/%m/%dT%H:%M"))

    activities = getAppActivitiesService()

    deliverables = (
        getDeliverablesByTeamService(g.user["team"]["id"])
        if "id" in g.user["team"]
        else []
    )
    deliverables = list(map(lambda x: x["activity"]["id"], deliverables))

    activities = list(
        filter(
            lambda activity: getDateTime(activity["start"], "T00:00") <= currentDate
            and (
                getDateTime(activity["end"]) >= currentDate
                or (activity["delay"] and getDateTime(activity["close"]) >= currentDate)
            )
            and activity["id"] not in deliverables,
            activities,
        )
    )

    return {"data": activities}
