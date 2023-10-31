from app import get_db
from bson.objectid import ObjectId
from utils.functions import cleanIds


def newDeliverableService(deliverable):
    db = get_db()

    db.deliverable.insert_one(deliverable)
    deliverable["id"] = str(deliverable.pop("_id"))

    return deliverable


def getDeliverablesByTeamService(team_id):
    db = get_db()

    deliverables = list(db.deliverable.find({"team": team_id}))
    cleanIds(deliverables)

    return deliverables


def getDeliverablesByActivityService(activity_id):
    db = get_db()

    deliverables = list(db.deliverable.find({"activity.id": activity_id}))
    cleanIds(deliverables)

    return deliverables
