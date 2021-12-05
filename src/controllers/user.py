from bson.objectid import ObjectId
from app import get_db, encode_auth_token
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
  res = {
    "auth_token": encode_auth_token(str(ObjectId(user["_id"]))),
    "email": user["email"],
    "name": user["name"]
  }
  return res