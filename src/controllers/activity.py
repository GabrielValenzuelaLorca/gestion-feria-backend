from flask import request
from flask_api import status
from services.activity import newActivityService

def newActivityController():
  activity = request.json

  activity = newActivityService(activity)

  activity['id'] = str(activity['_id'])
  del activity['_id']

  return activity