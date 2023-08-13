from flask import Blueprint
from .user import userRoute
from .activity import activityRoute
from .team import teamRoute
from .project import projectRoute
from .period import periodRoute

bp = Blueprint("/", __name__, url_prefix="/")
bp.register_blueprint(userRoute)
bp.register_blueprint(activityRoute)
bp.register_blueprint(teamRoute)
bp.register_blueprint(projectRoute)
bp.register_blueprint(periodRoute)
