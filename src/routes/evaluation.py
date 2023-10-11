from flask import Blueprint
from controllers.evaluation import getEvaluationsByActivityController
from wrappers import token_required

evaluationRoute = Blueprint("evaluation", __name__, url_prefix="/evaluation")


@evaluationRoute.route("/all/<activity_id>", methods=["GET"])
@token_required
def getEvaluationsByActivity(activity_id):
    return getEvaluationsByActivityController(activity_id)


# @evaluationRoute.route("/create/<activity_id>", methods=["POST"])
# @token_required
# def create(activity_id):
#     return newRubricController(activity_id)


# @evaluationRoute.route("/update/<activity_id>", methods=["PUT"])
# @token_required
# def edit(activity_id):
#     return editRubricController(activity_id)
