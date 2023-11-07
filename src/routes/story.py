from flask import Blueprint
from controllers.story import (
    createStoryController,
    getStoriesBySprintController,
    updateStateController,
)
from wrappers import token_required

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
