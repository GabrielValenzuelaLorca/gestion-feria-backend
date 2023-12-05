from flask import Blueprint
from controllers.team import (
    createController,
    dashboardController,
    getTeamController,
    updateController,
)
from wrappers import token_required

teamRoute = Blueprint("team", __name__, url_prefix="/team")


@teamRoute.route("/create", methods=["POST"])
@token_required
def create():
    return createController()


@teamRoute.route("/update", methods=["PUT"])
@token_required
def update():
    return updateController()


@teamRoute.route("/dashboard", methods=["GET"])
@token_required
def dashboard():
    return dashboardController()


@teamRoute.route("/<teamId>", methods=["GET"])
@token_required
def getTeam(teamId):
    return getTeamController(teamId)
