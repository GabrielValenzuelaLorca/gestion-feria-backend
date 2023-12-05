from flask import Blueprint
from src.controllers.deliverable import (
    evaluateController,
    getDeliverableByIdController,
    getDeliverablesByActivity,
    getDeliverablesByTeamController,
    newDeliverableController,
)
from src.wrappers import token_required

deliverableRoute = Blueprint("deliverable", __name__, url_prefix="/deliverable")


@deliverableRoute.route("/create/<activity_id>", methods=["POST"])
@token_required
def create(activity_id):
    return newDeliverableController(activity_id)


@deliverableRoute.route("/getByTeamId/<team_id>", methods=["GET"])
@token_required
def getByTeamId(team_id):
    return getDeliverablesByTeamController(team_id)


@deliverableRoute.route("/getByActivity/<activity_id>", methods=["GET"])
@token_required
def getByActivity(activity_id):
    return getDeliverablesByActivity(activity_id)


@deliverableRoute.route("/<deliverable_id>", methods=["GET"])
@token_required
def get(deliverable_id):
    return getDeliverableByIdController(deliverable_id)


@deliverableRoute.route("/evaluate/<deliverable_id>", methods=["POST"])
@token_required
def evaluate(deliverable_id):
    return evaluateController(deliverable_id)
