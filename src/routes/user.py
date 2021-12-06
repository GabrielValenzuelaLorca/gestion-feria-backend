from flask import Blueprint
from controllers.user import loginService, registerService

userRoute = Blueprint('user', __name__, url_prefix='/user')

@userRoute.route('/register', methods=['POST'])
def register():
  return registerService()

@userRoute.route('/login', methods=['POST'])
def login():
  return loginService()