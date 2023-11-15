from flask import request
from flask_api import status
from services.story import (
    createStoryService,
    findHigherIndex,
    getStoriesBySprintService,
    updateStoriesService,
    updateStoryService,
)


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
        "state": "Por Hacer",
        "progress": 0,
        "points": 0,
        "criticality": "Opcional",
        "sprint": "Backlog",
        "criteria": [""],
        "responsables": [],
        "index": findHigherIndex("Backlog", "Por Hacer", story["team_id"]) + 1,
    }

    newStory = createStoryService(newStory)

    return {"data": newStory}


def getStoriesBySprintController():
    teamId = request.args.get("teamId")
    sprint = request.args.get("sprint")

    if teamId is None:
        return errorMessage("teamId")

    stories = getStoriesBySprintService(teamId, sprint)

    return {"data": stories}


def updateStateController():
    params = request.json
    if "sourceStories" not in params:
        return errorMessage("sourceStories")
    if "destStories" not in params:
        return errorMessage("destStories")
    if "story" not in params:
        return errorMessage("story")

    story = updateStoriesService(params)
    return {"data": story}


def updateStoryController(storyId):
    story = request.json
    if "team_id" not in story:
        return errorMessage("team_id")
    if "number" not in story:
        return errorMessage("number")
    if "title" not in story:
        return errorMessage("title")
    if "description" not in story:
        return errorMessage("description")
    if "progress" not in story:
        return errorMessage("progress")
    if "points" not in story:
        return errorMessage("points")
    if "criticality" not in story:
        return errorMessage("criticality")

    story["progress"] = int(story["progress"])
    story["points"] = int(story["points"])
    updateStoryService(storyId, story)

    return {"data": story}
