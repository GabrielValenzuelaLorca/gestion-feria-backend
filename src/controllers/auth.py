from app import get_db

def register():
  db = get_db()
  new_id = db.test_collection.insert_one({"test": "probando"}).inserted_id
  return "eso esta funcionando con id {}".format(new_id)