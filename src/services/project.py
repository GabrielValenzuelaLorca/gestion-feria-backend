from app import get_db

def createProjectService(project):
  db = get_db()

  db.project.insert_one(project)

  return project