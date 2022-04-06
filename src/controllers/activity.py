from flask import request
from flask_api import status
from bson import json_util
from services.activity import newActivityService, getActivitiesService

def newActivityController():
  activity = request.json

  activity = newActivityService(activity)

  activity['id'] = str(activity['_id'])
  del activity['_id']

  return activity

def getActivitiesController():
  activities = json_util.dumps(getActivitiesService())

  return activities