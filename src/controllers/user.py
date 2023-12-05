import json
from app import encode_auth_token
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_api import status
from src.services.period import findActivePeriodService
from src.services.user import (
    getUserByIdService,
    loginService,
    registerUserService,
    getAllUsersService,
    updateUserService,
)


def registerController():
    activePeriod = findActivePeriodService()
    if activePeriod is None:
        return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR
    user = {
        "email": request.json["email"],
        "name": request.json["name"],
        "lastName": request.json["lastName"],
        "campus": request.json["campus"],
        "password": generate_password_hash(request.json["password"]),
        "rol": "Alumno",
        "team": {},
        "period": activePeriod["id"],
    }

    user = registerUserService(user)

    id = str(user.pop("_id"))
    user["auth_token"] = encode_auth_token(id)
    user["id"] = id
    del user["password"]

    return {"data": user}


def loginController():
    user = loginService({"email": request.json["email"]})

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


def getUserController(id):
    try:
        user = getUserByIdService(id)
        user["auth_token"] = encode_auth_token(id)
        return {"data": user}
    except RuntimeError as e:
        return "Usuario no encontrado", status.HTTP_404_NOT_FOUND


def getAllController():
    activePeriod = findActivePeriodService()
    query = {}
    roles = request.args.get("roles")
    active = request.args.get("active")
    campus = request.args.get("campus")

    if roles is not None:
        query["rol"] = {"$in": json.loads(roles)}

    if active:
        query["period"] = activePeriod["id"]

    if campus is not None and campus != "all":
        query["campus"] = campus

    users = getAllUsersService(query)

    return {"data": users}


def updateController():
    user = request.json
    user = updateUserService(user)

    return {"data": user}
