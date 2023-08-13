from app import get_db
from bson.objectid import ObjectId


def newDeliverableService(deliverable):
    db = get_db()

    db.deliverable.insert_one(deliverable)

    return deliverable
