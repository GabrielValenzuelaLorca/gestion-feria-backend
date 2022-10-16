from app import get_db

def createTeamService(team):
  db = get_db()

  db.team.insert_one(team)

  return team