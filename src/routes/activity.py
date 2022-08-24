from flask import Blueprint
from controllers.activity import newActivityController, editActivityController, getActivitiesController
from wrappers import token_required

activityRoute = Blueprint('activity', __name__, url_prefix='/activity')

@activityRoute.route('/create', methods=['POST'])
@token_required
def create():
  return newActivityController()

@activityRoute.route('/edit', methods=['PUT'])
@token_required
def edit():
  return editActivityController()

@activityRoute.route('', methods=['GET'])
@token_required
def get():
  return getActivitiesController()