from app import get_db
from bson.objectid import ObjectId

def registerService(user):
  db = get_db()

  db.user.insert_one(user)

  return user

def loginService(user):
  db = get_db()

  return db.user.find_one(user)

def getAllService():
  db = get_db()

  return db.user.find({}, {"password": False})

def updateService(user):
  db = get_db()

  id = ObjectId(user.pop("id"))
  db.user.update({"_id": id}, {"$set": user})

  return user