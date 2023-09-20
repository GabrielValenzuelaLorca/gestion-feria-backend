from app import get_db
from bson.objectid import ObjectId
from utils.functions import cleanIds
from services.period import findActivePeriodService

def newActivityService(activity):
  db = get_db()
  activity["close"] = activity["close"] if activity["close"] != '' else None
  db.activity.insert_one(activity)
  activity['id'] = str(activity.pop('_id'))

  return activity

def editActivityService(activity):
  db = get_db()
  id = activity.pop("id")
  db.activity.update_one({"_id": ObjectId(id)}, {"$set": activity})
  activity["id"] = id

  return activity

def getActivitiesService():
  db = get_db()
  activePeriod = findActivePeriodService()
  activities = list(db.activity.find({"period": activePeriod["id"]}))
  cleanIds(activities)

  return activities
