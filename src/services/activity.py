from app import get_db
from bson.objectid import ObjectId
from flask import g
from src.utils.functions import cleanIds
from src.services.period import findActivePeriodService


def newActivityService(activity):
    db = get_db()
    db.activity.insert_one(activity)
    activity["id"] = str(activity.pop("_id"))

    return activity


def editActivityService(activity):
    db = get_db()
    id = activity.pop("id")
    db.activity.update_one({"_id": ObjectId(id)}, {"$set": activity})
    activity["id"] = id

    return activity


def getActivityService(activity_id):
    db = get_db()
    activity = db.activity.find_one(ObjectId(activity_id))
    activity["id"] = str(activity.pop("_id"))

    return activity


def getActivitiesService():
    db = get_db()
    activePeriod = findActivePeriodService()
    query = {"period": activePeriod["id"]}
    if g.user["campus"] != "all":
        query["campus"] = {"$in": [g.user["campus"], "all"]}
    activities = list(db.activity.find(query))
    cleanIds(activities)

    return activities


def getPendingActivities(deliverable_ids, campus):
    db = get_db()
    deliverable_ids = list(map(lambda x: ObjectId(x), deliverable_ids))
    activePeriod = findActivePeriodService()
    activities = list(
        db.activity.find(
            {
                "_id": {"$nin": deliverable_ids},
                "period": activePeriod["id"],
                "campus": {"$in": [campus, "all"]},
            }
        )
    )
    cleanIds(activities)

    return activities


def getAppActivitiesService():
    db = get_db()

    activePeriod = findActivePeriodService()
    query = {
        "period": activePeriod["id"],
        "type": {
            "$in": [
                "storyCreation",
                "storyEdition",
                "storyAssign",
                "sprint",
            ]
        },
    }
    if g.user["campus"] != "all":
        query["campus"] = {"$in": [g.user["campus"], "all"]}
    activities = list(db.activity.find(query))

    cleanIds(activities)

    return activities
