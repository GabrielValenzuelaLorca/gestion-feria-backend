from app import encode_auth_token
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_api import status
from services.user import loginService, registerService, getAllService
from utils.functions import cleanIds

def registerController():
  user = {
    "email": request.json["email"],
    "name": request.json["name"],
    "password": generate_password_hash(request.json["password"])
  }

  user = registerService(user)

  res = {
    "auth_token": encode_auth_token(str(user["_id"])),
    "email": user["email"],
    "name": user["name"]
  }

  return {"data": res}

def loginController():
  user = loginService({
    "email": request.json["email"]
  })

  if user is None:
    return "Usuario no encontrado", status.HTTP_404_NOT_FOUND

  elif not check_password_hash(user["password"], request.json["password"]):  
    return "Contraseña incorrecta", status.HTTP_401_UNAUTHORIZED
    
  else:
    res = {
      "auth_token": encode_auth_token(str(user["_id"])),
      "email": user["email"],
      "name": user["name"]
    }
    return {"data": res}

def getAllController():
  users = list(getAllService())
  cleanIds(users)

  return {"data": users}