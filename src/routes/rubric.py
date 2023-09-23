from flask import Blueprint
from controllers.rubric import editRubricController, newRubricController
from wrappers import token_required

rubricRoute = Blueprint("rubric", __name__, url_prefix="/rubric")


@rubricRoute.route("/create/<activity_id>", methods=["POST"])
@token_required
def create(activity_id):
    return newRubricController(activity_id)


@rubricRoute.route("/update/<activity_id>", methods=["PUT"])
@token_required
def edit(activity_id):
    return editRubricController(activity_id)
