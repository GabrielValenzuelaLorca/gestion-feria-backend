from flask import Blueprint
from .user import userRoute
from .activity import activityRoute
from .team import teamRoute

bp = Blueprint('/', __name__, url_prefix='/')
bp.register_blueprint(userRoute)
bp.register_blueprint(activityRoute)
bp.register_blueprint(teamRoute)