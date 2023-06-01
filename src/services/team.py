from app import get_db
from bson.objectid import ObjectId


def getTeamService(id):
    db = get_db()

    return db.team.find_one({"_id": id})


def createTeamService(team):
    db = get_db()

    db.team.insert_one(team)

    return team


def updateTeamService(team):
    db = get_db()

    id = ObjectId(team.pop("id"))

    db.team.update({"_id": id}, {"$set": team})

    team["id"] = str(id)

    return team
