from flask import Blueprint
from controllers.team import createController
from wrappers import token_required

teamRoute = Blueprint('team', __name__, url_prefix='/team')

@teamRoute.route('/create', methods=['POST'])
@token_required
def create():
  return createController()