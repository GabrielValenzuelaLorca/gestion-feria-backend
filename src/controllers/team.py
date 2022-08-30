from flask import request, g
from services.team import createService
from services.user import getAllService, updateManyService
from utils.functions import cleanIds
from bson.objectid import ObjectId

def createController():
  team = request.json
  members = list(map(lambda user: ObjectId(user), team.pop("members")))

  team = createService(team)
  team["id"] = str(team.pop("_id"))

  updateManyService(members, {"team": team})

  user = list(getAllService({
    "_id": g.user["_id"]
  }))[0]

  user["id"] = str(user.pop("_id"))

  return {"data": user}