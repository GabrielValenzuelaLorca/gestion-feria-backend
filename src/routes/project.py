from flask import Blueprint
from controllers.project import updateProjectController
from wrappers import token_required

projectRoute = Blueprint("project", __name__, url_prefix="/project")


@projectRoute.route("/update", methods=["PUT"])
@token_required
def update():
    return updateProjectController()
