from app import get_db
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