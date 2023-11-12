from app import get_db
from bson.objectid import ObjectId

from utils.functions import cleanIds


def createStoryService(story):
    db = get_db()

    db.story.insert_one(story)
    story["id"] = str(story.pop("_id"))

    return story


def findHigherIndex(sprint, state, team_id):
    db = get_db()

    index = list(
        db.story.find(
            {"state": state, "sprint": sprint, "team_id": team_id}, {"index": 1}
        )
        .sort("index", -1)
        .limit(1)
    )

    return -1 if len(index) == 0 else index.pop()["index"]


def getStoriesBySprintService(teamId, sprint):
    db = get_db()

    filter = {"team_id": teamId}
    if sprint:
        filter["sprint"] = sprint

    stories = list(db.story.find(filter))
    cleanIds(stories)

    return stories


def updateStoriesService(params):
    db = get_db()

    params["sourceStories"] = list(map(lambda x: ObjectId(x), params["sourceStories"]))
    params["destStories"] = list(map(lambda x: ObjectId(x), params["destStories"]))

    db.story.update_many(
        {"_id": {"$in": params["sourceStories"]}},
        {"$inc": {"index": -1}},
    )
    db.story.update_many(
        {"_id": {"$in": params["destStories"]}},
        {"$inc": {"index": 1}},
    )
    db.story.update_one(
        {"_id": ObjectId(params["story"]["id"])},
        {
            "$set": {
                "state": params["story"]["state"],
                "index": params["story"]["index"],
            }
        },
    )


def updateStoryService(storyId, story):
    db = get_db()

    db.story.update_one({"_id": ObjectId(storyId)}, {"$set": story})
