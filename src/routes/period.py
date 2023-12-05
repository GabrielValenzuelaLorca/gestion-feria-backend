from flask import Blueprint
from src.controllers.period import createPeriodController, getActivePeriodController
from src.wrappers import token_required

periodRoute = Blueprint("period", __name__, url_prefix="/period")


@periodRoute.route("/create", methods=["POST"])
@token_required
def create():
    return createPeriodController()


@periodRoute.route("/active", methods=["GET"])
def getActive():
    return getActivePeriodController()
