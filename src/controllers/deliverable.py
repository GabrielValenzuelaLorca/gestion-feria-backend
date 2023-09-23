from datetime import datetime
from pytz import timezone
from flask import g
from flask_api import status
from services.deliverable import getDeliverablesByTeamService, newDeliverableService
from services.activity import getActivityService, getPendingActivities

tz = timezone("America/Santiago")
format = "%Y/%m/%dT%H:%M"


def getDateTime(date):
    return tz.localize(datetime.strptime(date + "T23:59", format))


def newDeliverableController(activity_id):
    currentDate = datetime.now(tz)
    activity = getActivityService(activity_id)
    endDate = getDateTime(activity["end"])
    deliverable = {
        "activity": activity,
        "date": datetime.strftime(currentDate, format + ".%z"),
        "team": g.user["team"]["id"],
    }

    if currentDate > endDate:
        if activity["delay"] and currentDate < getDateTime(activity["close"]):
            state = "done_delayed"
        else:
            return "Envío cerrado", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        state = "done"

    deliverable["state"] = state
    deliverable = newDeliverableService(deliverable)

    return {"data": deliverable}


def getDeliverablesByTeamController(team_id):
    currentDate = datetime.now(tz)

    def activityParser(activity):
        endDate = getDateTime(activity["end"])

        if currentDate > endDate:
            if activity["delay"] and currentDate < getDateTime(activity["close"]):
                state = "pending_delayed"
            else:
                state = "closed"
        else:
            state = "pending"

        return {**activity, "state": state, "send_date": None, "deliverable_id": None}

    deliverables = getDeliverablesByTeamService(team_id)

    deliverableIds = list(map(lambda x: x["activity"]["id"], deliverables))

    activities = getPendingActivities(deliverableIds)

    deliverablesAsActivities = list(
        map(
            lambda x: {
                "deliverable_id": x["id"],
                **x["activity"],
                "state": x["state"],
                "send_date": x["date"],
            },
            deliverables,
        )
    )
    deliverablesAsActivities.sort(key=lambda x: x["end"])

    activities = list(map(activityParser, activities))
    closedActivities = list(filter(lambda x: x["state"] == "closed", activities))
    closedActivities.sort(key=lambda x: x["end"])
    pendingActivities = list(filter(lambda x: x["state"] == "pending", activities))
    pendingActivities.sort(key=lambda x: x["end"])

    return {"data": pendingActivities + deliverablesAsActivities + closedActivities}