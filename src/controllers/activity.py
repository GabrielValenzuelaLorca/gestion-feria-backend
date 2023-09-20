from flask import request
from flask_api import status
from services.activity import editActivityService, newActivityService, getActivitiesService
from services.period import findActivePeriodService

def newActivityController():
  activity = request.json
  activePeriod = findActivePeriodService()

  if activePeriod is None:
      return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR
  
  activity["period"] = activePeriod["id"]
  activity = newActivityService(activity)

  return {"data": activity}

def editActivityController():
  activity = request.json
  activity = editActivityService(activity)

  return {"data": activity}

def getActivitiesController():
  activities = getActivitiesService()

  return {"data": activities}