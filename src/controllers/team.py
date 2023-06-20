from flask import request, g
from services.project import createProjectService
from services.team import createTeamService, updateTeamService, getTeamByIdService
from services.user import getAllService, updateManyService
from bson.objectid import ObjectId


def createController():
    project = createProjectService(
        {
            "name": None,
            "description": None,
            "email": None,
            "facebook": None,
            "instagram": None,
            "youtube": None,
            "webpage": None,
        }
    )
    project["id"] = str(project.pop("_id"))

    team = request.json
    team["linkedin"] = None
    team["project"] = project

    team = createTeamService(team)
    team["id"] = str(team.pop("_id"))

    members = list(map(lambda user: ObjectId(user), team["members"]))

    updateManyService(members, {"team": team})

    user = list(getAllService({"_id": g.user["_id"]}))[0]

    user["id"] = str(user.pop("_id"))

    return {"data": user}


def updateController():
    team = request.json
    oldTeam = getTeamByIdService(ObjectId(team["id"]))
    oldMembers = set(oldTeam.pop("members"))
    newMembers = team["members"]
    deleteMembers = list(oldMembers - set(newMembers))
    team["project"] = oldTeam["project"]

    team = updateTeamService(team)

    newMembers = list(map(lambda user: ObjectId(user), newMembers))
    deleteMembers = list(map(lambda user: ObjectId(user), deleteMembers))

    updateManyService(newMembers, {"team": team})
    updateManyService(deleteMembers, {"team": {}})

    user = list(getAllService({"_id": g.user["_id"]}))[0]

    user["id"] = str(user.pop("_id"))

    return {"data": user}
