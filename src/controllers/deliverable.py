import datetime
from flask import request
from flask_api import status
from services.period import findActivePeriodService
from services.deliverable import getDeliverablesByTeamService
from services.activity import getPendingActivities

# def newActivityController():
#   activity = request.json
#   activePeriod = findActivePeriodService()

#   if activePeriod is None:
#       return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR
  
#   activity["period"] = activePeriod["id"]
#   activity = newActivityService(activity)

#   return {"data": activity}

# def editActivityController():
#   activity = request.json
#   activity = editActivityService(activity)

#   return {"data": activity}

def getDeliverablesByTeamController(team_id):
  currentDate = datetime.datetime.now()
  def activityParser(activity):
    format = "%Y-%m-%dT%H:%M"
    endDate = datetime.datetime.strptime(activity["end"] + "T23:59", format)

    if currentDate > endDate:
      if activity["delay"]: 
        closeDate = datetime.datetime.strptime(activity["close"] + "T23:59", format)
        state = "closed" if currentDate > closeDate else "pending_delayed"
      else:
        state = "closed"
    else:
      state = "pending"
      
    return {**activity, "state": state, "send_date": None}
    
  deliverables = getDeliverablesByTeamService(team_id)
  deliverableIds = list(map(lambda x: x["activity"]["id"], deliverables))

  activities = getPendingActivities(deliverableIds)

  deliverablesAsActivities = list(map(lambda x: {**x["activity"], "state": x["state"], "send_date": x["date"]}, deliverables))
  deliverablesAsActivities.sort(key=lambda x: x["end"])

  activities = list(map(activityParser, activities))
  closedActivities = list(filter(lambda x: x["state"] == "closed", activities))
  closedActivities.sort(key=lambda x: x["end"])
  pendingActivities = list(filter(lambda x: x["state"] == "pending", activities))
  pendingActivities.sort(key=lambda x: x["end"])

  return {"data": pendingActivities + deliverablesAsActivities + closedActivities}