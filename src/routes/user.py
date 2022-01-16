from flask import Blueprint
from controllers.user import loginController, registerController

userRoute = Blueprint('user', __name__, url_prefix='/user')

@userRoute.route('/register', methods=['POST'])
def register():
  return registerController()

@userRoute.route('/login', methods=['POST'])
def login():
  return loginController()