from functools import wraps
from flask import request, g
from app import decode_auth_token, get_db
from bson.objectid import ObjectId

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'Authorization' in request.headers:
      token = request.headers['Authorization'].replace('Bearer ', '')
    if not token:
      return 'Unauthorized Access!', 401

    try:
      db = get_db()
      data = decode_auth_token(token)
      current_user = db.user.find_one({'_id': ObjectId(data)})
      if not current_user:
        return 'Unauthorized Access!', 401
      else:
        g.user = current_user
    except:
      return 'Unauthorized Access!', 401
    return f(*args, **kwargs)

  return decorated