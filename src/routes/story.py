from flask import Blueprint
from src.controllers.story import (
    createStoryController,
    getStoriesBySprintController,
    updateStateController,
    updateStoryController,
)
from src.wrappers import token_required

storyRoute = Blueprint("story", __name__, url_prefix="/story")


@storyRoute.route("/create", methods=["POST"])
@token_required
def create():
    return createStoryController()


@storyRoute.route("/getStoriesBySprint", methods=["GET"])
@token_required
def getStoriesBySprint():
    return getStoriesBySprintController()


@storyRoute.route("/updateState", methods=["PUT"])
@token_required
def updateState():
    return updateStateController()


@storyRoute.route("/update/<storyId>", methods=["PUT"])
@token_required
def update(storyId):
    return updateStoryController(storyId)
