from datetime import datetime
from json import dumps
from pytz import timezone
from flask import g, request
from flask_api import status
from services.deliverable import (
    evaluateService,
    getDeliverableByIdService,
    getDeliverablesByActivityService,
    getDeliverablesByTeamService,
    newDeliverableService,
)
from services.activity import getActivityService, getPendingActivities
from services.story import getStoriesBySprintService
from services.team import getNotEvaluatedTeamsService, getTeamByIdService
from services.user import getUserByIdService

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
    currentDate = datetime.now(tz)
    activity = getActivityService(activity_id)
    endDate = getDateTime(activity["end"])

    deliverable = {
        "activity": activity,
        "date": datetime.strftime(currentDate, format + ".%z"),
        "team": g.user["team"]["id"],
    }

    if activity["type"] == "sprint":
        deliverable["evaluation"] = getSprintEvaluation(activity, g.user["team"]["id"])

    if currentDate > endDate:
        if activity["delay"] and currentDate < getDateTime(activity["close"]):
            state = "done_delayed"
        else:
            return "Envío cerrado", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        state = "done"

    deliverable["state"] = state
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

        if currentDate > endDate:
            if activity["delay"] and currentDate < getDateTime(activity["close"]):
                state = "pending_delayed"
            else:
                state = "closed"
        else:
            state = "pending"

        return {**activity, "state": state, "send_date": None, "deliverable_id": None}

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

    if currentDate > endDate:
        if activity["delay"] and currentDate < getDateTime(activity["close"]):
            newState = "pending_delayed"
        else:
            newState = "closed"
    else:
        newState = "pending"

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
            finalScore = round((sum(storiesScores) / totalPoints) / 4, 2) * 100
        else:
            finalScore = 0
        evaluation["score"] = finalScore
        evaluateService(deliverable_id, evaluation)

    return {"data": evaluation}
