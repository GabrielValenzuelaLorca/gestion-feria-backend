from flask import Blueprint
from .user import userRoute
from.activity import activityRoute

bp = Blueprint('/', __name__, url_prefix='/')
bp.register_blueprint(userRoute)
bp.register_blueprint(activityRoute)