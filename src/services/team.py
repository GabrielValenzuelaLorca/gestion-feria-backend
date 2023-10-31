from app import get_db
from bson.objectid import ObjectId

from services.period import findActivePeriodService
from utils.functions import cleanIds


def getTeamByIdService(id):
    db = get_db()

    team = db.team.find_one({"_id": ObjectId(id)})
    team["id"] = str(team.pop("_id"))

    return team


def getTeamService(query):
    db = get_db()

    return db.team.find_one(query)


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


def getNotEvaluatedTeamsService(team_ids):
    db = get_db()
    team_ids = list(map(lambda x: ObjectId(x), team_ids))
    activePeriod = findActivePeriodService()
    teams = list(
        db.team.find(
            {
                "_id": {"$nin": team_ids},
                "period": activePeriod["id"],
            }
        )
    )
    cleanIds(teams)

    return teams
