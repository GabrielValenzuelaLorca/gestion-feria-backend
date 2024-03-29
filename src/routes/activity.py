from flask import Blueprint
from src.controllers.activity import (
    getActivityController,
    getAppActivitiesController,
    newActivityController,
    editActivityController,
    getActivitiesController,
)
from src.wrappers import token_required

activityRoute = Blueprint("activity", __name__, url_prefix="/activity")


@activityRoute.route("/create", methods=["POST"])
@token_required
def create():
    return newActivityController()


@activityRoute.route("/edit", methods=["PUT"])
@token_required
def edit():
    return editActivityController()


@activityRoute.route("", methods=["GET"])
@token_required
def get():
    return getActivitiesController()


@activityRoute.route("/<activity_id>", methods=["GET"])
@token_required
def getActivity(activity_id):
    return getActivityController(activity_id)


@activityRoute.route("/getAppActivities", methods=["GET"])
@token_required
def getAppActivities():
    return getAppActivitiesController()
