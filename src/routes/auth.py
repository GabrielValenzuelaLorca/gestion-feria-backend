from flask import Blueprint
from controllers.auth import register

authRoute = Blueprint('auth', __name__, url_prefix='/auth')

@authRoute.route('/register', methods=('GET', 'POST'))
def registerApp():
  return register()