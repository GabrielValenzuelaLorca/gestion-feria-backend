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
    "rol": "Alumno",
    "team": {}
  }

  user = registerService(user)

  id = str(user.pop("_id"))
  user["auth_token"] = encode_auth_token(id)
  user["id"] = id
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
    id = str(user.pop("_id"))
    user["auth_token"] = encode_auth_token(id)
    user["id"] = id
    del user["password"]

    return {"data": user}

def getAllController():
  query = {}
  rol = request.args.get('rol')

  if rol is not None:
    query["rol"] = rol

  users = list(getAllService(query))
  cleanIds(users)

  return {"data": users}

def updateController():
  user = request.json
  user = updateService(user)

  return {"data": user}