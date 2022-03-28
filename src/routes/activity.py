from flask import Blueprint
from controllers.activity import newActivityController
from wrappers import token_required

activityRoute = Blueprint('activity', __name__, url_prefix='/activity')

@activityRoute.route('/create', methods=['POST'])
@token_required
def create():
  return newActivityController()