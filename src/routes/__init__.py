from flask import Blueprint
from .user import userRoute

bp = Blueprint('/', __name__, url_prefix='/')
bp.register_blueprint(userRoute)