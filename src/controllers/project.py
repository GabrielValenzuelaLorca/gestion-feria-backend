from flask import request, g
from services.project import updateProjectService
from services.team import getTeamService, updateTeamService
from services.user import getAllService, updateManyService
from bson.objectid import ObjectId


def updateProjectController():
    project = request.json
    team = getTeamService({"project.id": project["id"]})
    membersIds = list(map(lambda user: ObjectId(user), team.pop("members")))

    project = updateProjectService(project)
    team["project"] = project
    team = updateTeamService(team)

    updateManyService(membersIds, {"team": team})

    user = list(getAllService({"_id": g.user["_id"]}))[0]

    user["id"] = str(user.pop("_id"))

    return {"data": user}
