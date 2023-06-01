from flask import Blueprint
from controllers.user import loginController, registerController, getAllController, updateController
from wrappers import token_required

userRoute = Blueprint('user', __name__, url_prefix='/user')

@userRoute.route('/register', methods=['POST'])
def register():
  return registerController()

@userRoute.route('/login', methods=['POST'])
def login():
  return loginController()

@userRoute.route('/all', methods=['GET'])
@token_required
def getAll():
  return getAllController()

@userRoute.route('/update', methods=['PUT'])
@token_required
def update():
  return updateController()