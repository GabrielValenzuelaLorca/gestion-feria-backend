from flask import Blueprint
from controllers.team import createController, updateController
from wrappers import token_required

teamRoute = Blueprint('team', __name__, url_prefix='/team')

@teamRoute.route('/create', methods=['POST'])
@token_required
def create():
  return createController()

@teamRoute.route('/update', methods=['PUT'])
@token_required
def update():
  return updateController()