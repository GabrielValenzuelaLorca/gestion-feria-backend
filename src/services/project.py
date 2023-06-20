from app import get_db
from bson.objectid import ObjectId


def createProjectService(project):
    db = get_db()

    db.project.insert_one(project)

    return project


def updateProjectService(project):
    db = get_db()

    id = ObjectId(project.pop("id"))

    db.project.update_one({"_id": id}, {"$set": project})

    project["id"] = str(id)

    return project
