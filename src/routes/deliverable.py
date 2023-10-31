from flask import Blueprint
from controllers.deliverable import (
    getDeliverablesByActivity,
    getDeliverablesByTeamController,
    newDeliverableController,
)
from wrappers import token_required

deliverableRoute = Blueprint("deliverable", __name__, url_prefix="/deliverable")


@deliverableRoute.route("/create/<activity_id>", methods=["POST"])
@token_required
def create(activity_id):
    return newDeliverableController(activity_id)


@deliverableRoute.route("/<team_id>", methods=["GET"])
@token_required
def get(team_id):
    return getDeliverablesByTeamController(team_id)


@deliverableRoute.route("/getByActivity/<activity_id>", methods=["GET"])
@token_required
def getByActivity(activity_id):
    return getDeliverablesByActivity(activity_id)
