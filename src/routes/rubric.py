from flask import Blueprint
from controllers.rubric import createAndUpdateRubricController
from wrappers import token_required

rubricRoute = Blueprint("rubric", __name__, url_prefix="/rubric")


@rubricRoute.route("/create/<activity_id>", methods=["POST"])
@token_required
def create(activity_id):
    return createAndUpdateRubricController(activity_id)


@rubricRoute.route("/update/<activity_id>", methods=["PUT"])
@token_required
def edit(activity_id):
    return createAndUpdateRubricController(activity_id)
