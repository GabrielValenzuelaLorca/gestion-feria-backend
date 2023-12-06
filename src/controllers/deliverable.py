import os
import boto3
from datetime import datetime
from pytz import timezone
from flask import g, request
from flask_api import status
from src.services.deliverable import (
    evaluateService,
    getDeliverableByIdService,
    getDeliverablesByActivityService,
    getDeliverablesByTeamService,
    newDeliverableService,
)
from src.services.activity import getActivityService, getPendingActivities
from src.services.story import getStoriesBySprintService
from src.services.team import getNotEvaluatedTeamsService, getTeamByIdService
from src.services.user import getUserByIdService
from src.utils.functions import errorMessage, saveLocalFile

tz = timezone("America/Santiago")
format = "%Y/%m/%dT%H:%M"


def getDateTime(date):
    return tz.localize(datetime.strptime(date + "T23:59", format))


def getSprintEvaluation(activity, teamId):
    details = {}
    evaluators = {}
    stories = getStoriesBySprintService(teamId, activity["name"])
    for evaluator in activity["evaluators"]:
        user = getUserByIdService(evaluator)
        evaluators[evaluator] = {"score": 0, "feedback": "", "rol": user["rol"]}
    for story in stories:
        details[story["id"]] = []
        for _ in story["criteria"]:
            details[story["id"]].append(evaluators)
    return {"score": 0, "feedback": "", "stories": details}


def newDeliverableController(activity_id):
    activity = getActivityService(activity_id)

    if "file" not in request.files and activity["type"] == "document":
        return errorMessage("file")
    elif "file" in request.files and activity["type"] == "document":
        file = request.files["file"]
        if file.filename == "":
            return errorMessage("file")
        if os.environ.get("FLASK_ENV") == "development":
            saveLocalFile(file, "deliverables")
        elif os.environ.get("FLASK_ENV") == "production":
            s3 = boto3.resource("s3")
            s3.Bucket("case-di-bucket").put_object(Key=file.filename, Body=file)
    currentDate = datetime.now(tz)
    endDate = getDateTime(activity["end"])

    deliverable = {
        "activity": activity,
        "date": datetime.strftime(currentDate, format + ".%z"),
        "team": g.user["team"]["id"],
        "state": "done",
    }

    if activity["type"] == "sprint":
        deliverable["evaluation"] = getSprintEvaluation(activity, g.user["team"]["id"])

    if currentDate > endDate:
        if activity["delay"] and currentDate < getDateTime(activity["close"]):
            delayed = True
        else:
            return "Envío cerrado", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        delayed = False

    deliverable["delayed"] = delayed
    deliverable = newDeliverableService(deliverable)

    return {"data": deliverable}


def getDeliverableByIdController(deliverable_id):
    deliverable = getDeliverableByIdService(deliverable_id)
    return {"data": deliverable}


def getDeliverablesByTeamController(team_id):
    team = getTeamByIdService(team_id)
    currentDate = datetime.now(tz)

    def activityParser(activity):
        endDate = getDateTime(activity["end"])

        state = "pending"
        delayed = False
        if currentDate > endDate:
            if activity["delay"] and currentDate < getDateTime(activity["close"]):
                delayed = True
            else:
                state = "closed"

        return {
            **activity,
            "state": state,
            "delayed": delayed,
            "send_date": None,
            "deliverable_id": None,
        }

    deliverables = getDeliverablesByTeamService(team_id)

    deliverableIds = list(map(lambda x: x["activity"]["id"], deliverables))

    activities = getPendingActivities(deliverableIds, team["campus"])

    deliverablesAsActivities = list(
        map(
            lambda x: {
                "deliverable_id": x["id"],
                **x["activity"],
                "state": x["state"],
                "send_date": x["date"],
            },
            deliverables,
        )
    )
    deliverablesAsActivities.sort(key=lambda x: x["end"])

    activities = list(map(activityParser, activities))
    closedActivities = list(filter(lambda x: x["state"] == "closed", activities))
    closedActivities.sort(key=lambda x: x["end"])
    pendingActivities = list(filter(lambda x: x["state"] == "pending", activities))
    pendingActivities.sort(key=lambda x: x["end"])

    return {"data": pendingActivities + deliverablesAsActivities + closedActivities}


def getDeliverablesByActivity(activity_id):
    currentDate = datetime.now(tz)
    activity = getActivityService(activity_id)
    endDate = getDateTime(activity["end"])

    newState = "pending"
    delayed = False
    if currentDate > endDate:
        if activity["delay"] and currentDate < getDateTime(activity["close"]):
            delayed = True
        else:
            newState = "closed"

    deliverables = getDeliverablesByActivityService(activity_id)
    deliverablesWithTeam = list(
        map(
            lambda x: {**x, "team": getTeamByIdService(x["team"])},
            deliverables,
        )
    )

    deliveredTeams = list(map(lambda x: x["team"], deliverables))

    notEvaluatedTeams = getNotEvaluatedTeamsService(deliveredTeams, activity["campus"])
    notEvaluatedTeams = list(
        map(
            lambda x: {
                "team": x,
                "evaluation": None,
                "date": None,
                "state": newState,
                "delayed": delayed,
                "activity": activity,
            },
            notEvaluatedTeams,
        )
    )

    allTeams = deliverablesWithTeam + notEvaluatedTeams
    allTeams.sort(key=lambda x: x["team"]["name"])

    return {"data": {"activity": activity, "deliverables": allTeams}}


def evaluateController(deliverable_id):
    evaluation = request.json
    deliverable = getDeliverableByIdService(deliverable_id)
    if deliverable["activity"]["type"] != "sprint":
        evaluateService(deliverable_id, evaluation)
    else:
        storiesScores = []
        totalPoints = 0

        for storyId, criterias in deliverable["evaluation"]["stories"].items():
            for i, criteria in enumerate(criterias):
                for evaluator, evaluationInstance in criteria.items():
                    if evaluator != str(g.user["_id"]):
                        evaluation["stories"][storyId][i][
                            evaluator
                        ] = evaluationInstance

        stories = getStoriesBySprintService(
            deliverable["team"], deliverable["activity"]["name"]
        )

        for story in stories:
            totalPoints += story["points"]
            profesorStoryScore = []
            ayudanteStoryScore = []
            for criteria in evaluation["stories"][story["id"]]:
                for criteriaEvaluation in criteria.values():
                    if criteriaEvaluation["rol"] == "Profesor":
                        profesorStoryScore.append(criteriaEvaluation["score"])
                    if criteriaEvaluation["rol"] == "Ayudante":
                        ayudanteStoryScore.append(criteriaEvaluation["score"])
            profesorMean = (
                sum(profesorStoryScore) / len(profesorStoryScore)
                if len(profesorStoryScore) > 0
                else 4
            ) * 0.7
            ayudanteMean = (
                sum(ayudanteStoryScore) / len(ayudanteStoryScore)
                if len(ayudanteStoryScore) > 0
                else 4
            ) * 0.3
            factor = (profesorMean + ayudanteMean) * story["points"]
            storiesScores.append(factor)
        if totalPoints > 0:
            finalScore = round((sum(storiesScores) / totalPoints) * 100 / 4, 0)
        else:
            finalScore = 0
        evaluation["score"] = finalScore
        evaluateService(deliverable_id, evaluation)

    return {"data": evaluation}
