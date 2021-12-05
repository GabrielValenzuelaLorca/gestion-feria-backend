from bson.objectid import ObjectId
from app import get_db
from flask import request
from werkzeug.security import generate_password_hash

def registerService():
  db = get_db()
  
  user = {
    "email": request.json["email"],
    "name": request.json["name"],
    "password": generate_password_hash(request.json["password"])
  }
  db.user.insert_one(user)
  user["_id"] = str(ObjectId(user["_id"]))
  del user['password']
  return user