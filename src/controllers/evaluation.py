from flask import request
from services.activity import getActivityService
from services.evaluation import getEvaluationsByActivityService
from services.team import getNotEvaluatedTeamsService


def getEvaluationsByActivityController(activity_id):
    activity = getActivityService(activity_id)
    evaluations = getEvaluationsByActivityService(activity_id)
    evaluationsAsTeams = list(
        map(
            lambda x: {**x["team"], "score": x["score"], "evaluation_id": x["id"]},
            evaluations,
        )
    )
    evaluatedTeams = list(map(lambda x: x["team"]["id"], evaluations))

    notEvaluatedTeams = getNotEvaluatedTeamsService(evaluatedTeams)
    notEvaluatedTeams = list(
        map(lambda x: {**x, "score": None, "evaluation_id": None}, notEvaluatedTeams)
    )

    allTeams = evaluationsAsTeams + notEvaluatedTeams
    allTeams.sort(key=lambda x: x["name"])

    return {"data": {"activity": activity, "evaluations": allTeams}}
