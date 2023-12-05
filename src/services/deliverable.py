from app import get_db
from bson.objectid import ObjectId
from src.utils.functions import cleanIds


def newDeliverableService(deliverable):
    db = get_db()

    db.deliverable.insert_one(deliverable)
    deliverable["id"] = str(deliverable.pop("_id"))

    return deliverable


def updateDeliverablesService(query, deliverable):
    db = get_db()

    db.deliverable.update_many(query, {"$set": deliverable})
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


def getDeliverableByIdService(deliverable_id):
    db = get_db()

    deliverable = db.deliverable.find_one(ObjectId(deliverable_id))
    deliverable["id"] = str(deliverable.pop("_id"))

    return deliverable


def evaluateService(deliverable_id, evaluation):
    db = get_db()

    db.deliverable.update_one(
        {"_id": ObjectId(deliverable_id)},
        {"$set": {"evaluation": evaluation, "state": "evaluated"}},
    )

    return evaluation
