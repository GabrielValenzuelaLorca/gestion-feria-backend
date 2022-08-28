from app import encode_auth_token
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_api import status
from services.user import loginService, registerService, getAllService, updateService
from utils.functions import cleanIds

def registerController():
  user = {
    "email": request.json["email"],
    "name": request.json["name"],
    "password": generate_password_hash(request.json["password"]),
    "rol": "Alumno "
  }

  user = registerService(user)

  user["auth_token"] = str(user.pop("_id"))
  del user["password"]

  return {"data": user}

def loginController():
  user = loginService({
    "email": request.json["email"]
  })

  if user is None:
    return "Usuario no encontrado", status.HTTP_404_NOT_FOUND

  elif not check_password_hash(user["password"], request.json["password"]):  
    return "Contraseña incorrecta", status.HTTP_401_UNAUTHORIZED
    
  else:
    user["auth_token"] = encode_auth_token(str(user.pop("_id")))
    del user["password"]
    
    return {"data": user}

def getAllController():
  users = list(getAllService())
  cleanIds(users)

  return {"data": users}

def updateController():
  user = request.json
  user = updateService(user)

  return {"data": user}