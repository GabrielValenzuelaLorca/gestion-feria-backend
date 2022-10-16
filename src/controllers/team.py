from flask import request, g
from services.project import createProjectService
from services.team import createTeamService
from services.user import getAllService, updateManyService
from bson.objectid import ObjectId

def createController():
  team = request.json
  team['linkedin'] = None

  members = list(map(lambda user: ObjectId(user), team.pop("members")))

  team = createTeamService(team)
  team["id"] = str(team.pop("_id"))

  project = createProjectService({
    "name": None,
    "email": None,
    "facebook": None,
    "instagram": None,
    "youtube": None,
    "webpage": None
  })
  project["id"] = str(project.pop("_id"))

  updateManyService(members, {
    "team": team,
    "project": project
  })

  user = list(getAllService({
    "_id": g.user["_id"]
  }))[0]

  user["id"] = str(user.pop("_id"))

  return {"data": user}