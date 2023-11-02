from flask import request
from services.activity import editActivityService
from services.deliverable import updateDeliverablesService


def createAndUpdateRubricController(activity_id):
    rubric = request.json
    activity = {"id": activity_id, "rubric": rubric}
    editActivityService(activity)
    updateDeliverablesService({"activity.id": activity_id}, {"activity.rubric": rubric})

    return {"data": rubric}
