from app import get_db
from bson.objectid import ObjectId


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
    print("index", index)

    return -1 if len(index) == 0 else index.pop()["index"]
