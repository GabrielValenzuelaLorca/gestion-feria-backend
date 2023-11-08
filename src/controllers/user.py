from app import encode_auth_token
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_api import status
from services.period import findActivePeriodService
from services.user import (
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
    rol = request.args.get("rol")
    active = request.args.get("active")

    if rol is not None:
        query["rol"] = rol

    if active:
        query["period"] = activePeriod["id"]

    users = getAllUsersService(query)

    return {"data": users}


def updateController():
    user = request.json
    user = updateUserService(user)

    return {"data": user}
