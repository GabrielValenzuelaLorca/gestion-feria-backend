from flask import request
from flask_api import status
from services.activity import editActivityService, newActivityService, getActivitiesService
from services.period import findActivePeriodService
from utils.functions import cleanIds

def newActivityController():
  activity = request.json
  activePeriod = findActivePeriodService()

  if activePeriod is None:
      return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR
  
  activity["period"]=activePeriod
  activity = newActivityService(activity)
  activity['id'] = str(activity.pop('_id'))

  return {"data": activity}

def editActivityController():
  activity = request.json

  id = activity['id']
  newActivity = editActivityService(activity)
  newActivity['id'] = id 

  return {"data": activity}

def getActivitiesController():
  activities = list(getActivitiesService())
  cleanIds(activities)

  return {"data": activities}