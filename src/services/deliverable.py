from app import get_db
from bson.objectid import ObjectId
from utils.functions import cleanIds

# def newDeliverableService(deliverable):
#     db = get_db()

#     db.deliverable.insert_one(deliverable)

#     return deliverable

def getDeliverablesByTeamService(team_id):
  db = get_db()

  deliverables = list(db.deliverables.find({"team": team_id}))
  cleanIds(deliverables)
  
  return deliverables