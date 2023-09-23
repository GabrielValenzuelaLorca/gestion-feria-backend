from flask import Blueprint
from controllers.rubric import newRubricController
from wrappers import token_required

rubricRoute = Blueprint("rubric", __name__, url_prefix="/rubric")


@rubricRoute.route("/create/<activity_id>", methods=["POST"])
@token_required
def create(activity_id):
    return newRubricController(activity_id)
