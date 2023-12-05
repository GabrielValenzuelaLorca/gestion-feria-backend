from app import get_db
from bson.objectid import ObjectId

from utils.functions import cleanIds


def registerUserService(user):
    db = get_db()

    db.user.insert_one(user)

    return user


def loginService(user):
    db = get_db()

    return db.user.find_one(user)


def getUserByIdService(id):
    db = get_db()
    user = db.user.find_one(ObjectId(id), {"password": False})
    if user is None:
        raise RuntimeError
    user["id"] = str(user.pop("_id"))
    return user


def getAllUsersService(query):
    db = get_db()

    users = list(db.user.find(query, {"password": False}))
    cleanIds(users)
    return users


def updateUserService(user):
    db = get_db()

    id = ObjectId(user.pop("id"))
    db.user.update({"_id": id}, {"$set": user})

    return user


def updateManyUsersService(users, data):
    db = get_db()

    users = list(map(lambda userId: ObjectId(userId), users))

    db.user.update_many({"_id": {"$in": users}}, {"$set": data})

    return users
