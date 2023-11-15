from flask import request, g
from flask_api import status
from services.period import findActivePeriodService
from services.project import createProjectService
from services.story import getStoriesBySprintService
from services.team import (
    createTeamService,
    getAllTeamsService,
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
    team["campus"] = g.user["campus"]

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


def dashboardController():
    def mapCallback(team):
        team["progress"] = {}
        teamProgress = {"total": []}
        stories = getStoriesBySprintService(team["id"], None)
        for story in stories:
            if story["sprint"] not in teamProgress:
                teamProgress[story["sprint"]] = []
            teamProgress[story["sprint"]].append(story["progress"])
            if story["criticality"] != "Opcional" or story["sprint"] != "Backlog":
                teamProgress["total"].append(story["progress"])
        print(teamProgress)
        for sprint, progress in teamProgress.items():
            team["progress"][sprint] = sum(progress) / max(len(progress), 1)
        return team

    activePeriod = findActivePeriodService()

    query = {"period": activePeriod["id"]}
    if g.user["campus"] != "all":
        query["campus"] = g.user["campus"]
    teams = getAllTeamsService(query)
    teams = list(map(mapCallback, teams))
    return {"data": teams}


def getTeamController(teamId):
    return {"data": getTeamByIdService(teamId)}
