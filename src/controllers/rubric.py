from flask import request
from services.activity import editActivityService
from services.rubric import editRubricService, newRubricService


def newRubricController(activity_id):
    rubric = request.json
    rubric = newRubricService(rubric)
    activity = {"id": activity_id, "rubric": rubric}
    editActivityService(activity)

    return {"data": rubric}


def editRubricController(activity_id):
    rubric = request.json
    rubric = editRubricService(rubric)
    activity = {"id": activity_id, "rubric": rubric}
    editActivityService(activity)

    return {"data": rubric}
