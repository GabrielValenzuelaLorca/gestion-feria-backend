from app import get_db

def newActivityService(activity):
  db = get_db()

  db.activity.insert_one(activity)

  return activity

def getActivitiesService():
  db = get_db()

  activities = db.activity.find().limit(30)

  return activities