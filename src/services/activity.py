from app import get_db
from bson.objectid import ObjectId

def newActivityService(activity):
  db = get_db()
  activity["close"] = activity["close"] != '' or None

  db.activity.insert_one(activity)

  return activity

def editActivityService(activity):
  db = get_db()
  id = ObjectId(activity.pop("id"))
  db.activity.update_one({"_id": id}, {"$set": activity})

  return activity

def getActivitiesService():
  db = get_db()

  activities = db.activity.find().limit(30)

  return activities
