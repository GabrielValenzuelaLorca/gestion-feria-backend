from app import get_db

def registerService(user):
  db = get_db()

  db.user.insert_one(user)

  return user

def loginService(user):
  db = get_db()

  return db.user.find_one(user)