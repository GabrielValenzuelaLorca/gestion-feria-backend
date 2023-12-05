from flask_api import status
from werkzeug.utils import secure_filename
import os


def cleanIds(list):
    for element in list:
        element["id"] = str(element.pop("_id"))


def errorMessage(field):
    return "{0} not found".format(field), status.HTTP_400_BAD_REQUEST


CURRENT_DIRECTORY = os.getcwd() + "/"


def saveLocalFile(file, folder):
    filename = secure_filename(file.filename)
    if not os.path.exists(CURRENT_DIRECTORY + "tmp/" + folder):
        os.makedirs(CURRENT_DIRECTORY + "tmp/" + folder)
    file.save(os.path.join(CURRENT_DIRECTORY + "tmp/" + folder, filename))
