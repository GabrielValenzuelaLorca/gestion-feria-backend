from flask import request, g
from flask_api import status
from src.services.period import findActivePeriodService
from src.services.story import getStoriesBySprintService
from src.services.team import (
    createTeamService,
    getAllTeamsService,
    getTeamMembersService,
    updateTeamService,
    getTeamByIdService,
)
from src.services.user import getUserByIdService, updateManyUsersService


def createController():
    activePeriod = findActivePeriodService()

    if activePeriod is None:
        return "No existe periodo activo", status.HTTP_500_INTERNAL_SERVER_ERROR

    project = {
        "name": None,
        "description": None,
        "email": None,
        "facebook": None,
        "instagram": None,
        "youtube": None,
        "webpage": None,
    }

    team = request.json
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

    team = updateTeamService(team)

    updateManyUsersService(newMembers, {"team": team})
    updateManyUsersService(deleteMembers, {"team": {}})

    user = getUserByIdService(g.user["_id"])

    return {"data": user}


def dashboardController():
    def sumProgressPonderedWithPoints(stories):
        total = 0
        for story in stories:
            total += story["progress"] * story["points"]
        return total

    def mapCallback(team):
        team["progress"] = {}
        teamProgress = {"total": {"points": 0, "stories": []}}
        stories = getStoriesBySprintService(team["id"], None)
        for story in stories:
            if story["sprint"] not in teamProgress:
                teamProgress[story["sprint"]] = {"points": 0, "stories": []}
            teamProgress[story["sprint"]]["stories"].append(
                {"progress": story["progress"], "points": story["points"]}
            )
            teamProgress[story["sprint"]]["points"] += story["points"]
            if story["criticality"] != "Opcional" or story["sprint"] != "Backlog":
                teamProgress["total"]["stories"].append(
                    {"progress": story["progress"], "points": story["points"]}
                )
                teamProgress["total"]["points"] += story["points"]
        print(teamProgress)
        for sprint, info in teamProgress.items():
            team["progress"][sprint] = round(
                sumProgressPonderedWithPoints(info["stories"]) / max(info["points"], 1),
                2,
            )
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
