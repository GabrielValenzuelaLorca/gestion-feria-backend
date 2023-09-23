from app import get_db
from bson.objectid import ObjectId


def newRubricService(rubric):
    db = get_db()
    rubric = {"rows": rubric}
    db.rubric.insert_one(rubric)
    rubric["id"] = str(rubric.pop("_id"))

    return rubric


def editRubricService(rubric):
    db = get_db()
    id = rubric.pop("id")
    db.rubric.update_one({"_id": ObjectId(id)}, {"$set": rubric})
    rubric["id"] = id

    return rubric
