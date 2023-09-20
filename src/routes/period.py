from flask import Blueprint
from controllers.period import createPeriodController, getActivePeriodController
from wrappers import token_required

periodRoute = Blueprint("period", __name__, url_prefix="/period")


@periodRoute.route("/create", methods=["POST"])
@token_required
def create():
    return createPeriodController()

@periodRoute.route("/active", methods=["GET"])
@token_required
def getActive():
    return getActivePeriodController()