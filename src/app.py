from flask import Flask
from flask_pymongo import PyMongo
from flask import current_app, g
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI='mongodb://localhost:27017/gestion-feria'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from routes import bp
    app.register_blueprint(bp)

    return app

def get_db():
  if 'db' not in g:
    g.db = PyMongo(current_app).db

  return g.db