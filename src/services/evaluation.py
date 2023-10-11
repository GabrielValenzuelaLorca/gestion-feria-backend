from app import get_db
from utils.functions import cleanIds


def getEvaluationsByActivityService(activity_id):
    db = get_db()

    evaluations = list(db.evaluations.find({"activity": activity_id}))
    cleanIds(evaluations)

    return evaluations
