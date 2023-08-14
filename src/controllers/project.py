from flask import request, g
from services.project import updateProjectService
from services.team import getTeamService, updateTeamService
from services.user import updateManyUsersService, getUserByIdService


def updateProjectController():
    project = request.json
    project = updateProjectService(project)

    team = getTeamService({"project.id": project["id"]})
    membersIds = team["members"]
    team["project"] = project
    team["id"] = team.pop("_id")
    team = updateTeamService(team)

    updateManyUsersService(membersIds, {"team": team})

    user = getUserByIdService(g.user["_id"])

    return {"data": user}
