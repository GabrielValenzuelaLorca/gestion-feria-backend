from flask import Blueprint
from controllers.story import createStoryController
from wrappers import token_required

storyRoute = Blueprint("story", __name__, url_prefix="/story")


@storyRoute.route("/create", methods=["POST"])
@token_required
def create():
    return createStoryController()
