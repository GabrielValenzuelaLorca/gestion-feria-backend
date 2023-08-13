from flask import Blueprint
from controllers.period import createController
from wrappers import token_required

periodRoute = Blueprint("period", __name__, url_prefix="/period")


@periodRoute.route("/create", methods=["POST"])
@token_required
def create():
    return createController()
