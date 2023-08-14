from flask import Blueprint
from controllers.period import createPeriodController
from wrappers import token_required

periodRoute = Blueprint("period", __name__, url_prefix="/period")


@periodRoute.route("/create", methods=["POST"])
@token_required
def create():
    return createPeriodController()
