from flask import Blueprint
from .auth import authRoute

bp = Blueprint('/', __name__, url_prefix='/')
bp.register_blueprint(authRoute)