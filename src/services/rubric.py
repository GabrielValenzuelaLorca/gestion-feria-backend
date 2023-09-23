from app import get_db


def newRubricService(rubric):
    db = get_db()
    rubric = {"rows": rubric}
    db.rubric.insert_one(rubric)
    rubric["id"] = str(rubric.pop("_id"))

    return rubric
