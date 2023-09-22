from flask import Blueprint
from controllers.deliverable import getDeliverablesByTeamController
from wrappers import token_required

deliverableRoute = Blueprint("deliverable", __name__, url_prefix="/deliverable")


# @activityRoute.route("/create", methods=["POST"])
# @token_required
# def create():
#     return newActivityController()


# @activityRoute.route("/edit", methods=["PUT"])
# @token_required
# def edit():
#     return editActivityController()


@deliverableRoute.route("/<team_id>", methods=["GET"])
@token_required
def get(team_id):
    return getDeliverablesByTeamController(team_id)
