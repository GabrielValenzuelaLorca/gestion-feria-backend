from flask import request
from flask_api import status

from services.story import createStoryService, findHigherIndex


def errorMessage(field):
    return "{0} not found".format(field), status.HTTP_400_BAD_REQUEST


def createStoryController():
    story = request.json
    if "team_id" not in story:
        return errorMessage("team_id")
    if "number" not in story:
        return errorMessage("number")
    if "title" not in story:
        return errorMessage("title")
    if "description" not in story:
        return errorMessage("description")

    newStory = {
        **story,
        "number": int(story["number"]),
        "state": "to do",
        "progress": 0,
        "points": 0,
        "criticality": "optional",
        "sprint": "backlog",
        "criteria": "",
        "responsables": [],
        "index": findHigherIndex("backlog", "to do", story["team_id"]) + 1,
    }

    newStory = createStoryService(newStory)

    return {"data": newStory}
