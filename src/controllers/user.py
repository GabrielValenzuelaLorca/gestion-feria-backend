from bson.objectid import ObjectId
from app import get_db, encode_auth_token
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_api import status

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

def loginService():
  db = get_db()

  user = db.user.find_one({
    "email": request.json["email"]
  })

  if user is None:
    return "Usuario no encontrado", status.HTTP_404_NOT_FOUND

  elif not check_password_hash(user["password"], request.json["password"]):  
    return "Contraseña incorrecta", status.HTTP_401_UNAUTHORIZED
    
  else:
    res = {
      "auth_token": encode_auth_token(str(ObjectId(user["_id"]))),
      "email": user["email"],
      "name": user["name"]
    }
    return res