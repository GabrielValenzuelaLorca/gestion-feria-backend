from app import get_db
from bson.objectid import ObjectId
from utils.functions import cleanIds

def createService(team):
  db = get_db()

  db.team.insert_one(team)

  return team