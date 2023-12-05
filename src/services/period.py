from app import get_db
from bson.objectid import ObjectId


def createPeriodService(period):
    db = get_db()

    db.period.insert_one(period)

    period["id"] = str(period.pop("_id"))

    return period


def findActivePeriodService():
    db = get_db()

    period = db.period.find_one({"active": True})

    if period is not None:
        period["id"] = str(period.pop("_id"))

    return period


def updatePeriodService(period):
    db = get_db()

    id = ObjectId(period.pop("id"))

    db.period.update_one({"_id": id}, {"$set": period})

    period["id"] = str(id)

    return period
