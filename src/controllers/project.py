from flask import request, g
from services.project import updateProjectService
from services.team import getTeamService, updateTeamService
from services.user import updateManyUsersService, getUserByIdService


def updateProjectController():
    project = request.json
    team = getTeamService({"project.id": project["id"]})
    membersIds = team.pop("members")

    project = updateProjectService(project)
    team["project"] = project
    team = updateTeamService(team)

    updateManyUsersService(membersIds, {"team": team})

    user = getUserByIdService(g.user["_id"])
    user["id"] = str(user.pop("_id"))

    return {"data": user}
