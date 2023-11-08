from flask import request, g
from flask_api import status
from services.period import findActivePeriodService
from services.project import createProjectService
from services.team import (
    createTeamService,
    getTeamMembersService,
    updateTeamService,
    getTeamByIdService,
)
from services.user import getUserByIdService, updateManyUsersService


def createController():
    activePeriod = findActivePeriodService()

    if activePeriod is None:
        return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR

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
    team["period"] = activePeriod["id"]

    membersIds = team["members"]
    members = getTeamMembersService(membersIds)
    team["members"] = members

    team = createTeamService(team)
    team["id"] = str(team.pop("_id"))

    updateManyUsersService(membersIds, {"team": team})

    user = getUserByIdService(g.user["_id"])

    return {"data": user}


def updateController():
    team = request.json
    oldTeam = getTeamByIdService(team["id"])
    oldMembers = set(map(lambda x: x["id"], oldTeam["members"]))
    newMembers = team["members"]
    deleteMembers = list(oldMembers - set(newMembers))
    team["members"] = getTeamMembersService(newMembers)
    team["project"] = oldTeam["project"]

    team = updateTeamService(team)

    updateManyUsersService(newMembers, {"team": team})
    updateManyUsersService(deleteMembers, {"team": {}})

    user = getUserByIdService(g.user["_id"])

    return {"data": user}
