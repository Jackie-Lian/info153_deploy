from dotenv import load_dotenv
from flask import Flask
from db import db
import models
from models.task import TasksModel
from resources.tasks import blp as TasksBlueprint
from resources.user import blp as UserBlueprint
from flask_smorest import Api

import redis
from rq import Queue
import os

from flask_jwt_extended import JWTManager

app = Flask(__name__)
load_dotenv()

jwt = JWTManager(app)
connection = redis.from_url(os.getenv("REDIS_URL"))
app.queue = Queue("emails", connection=connection)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["JWT_SECRET_KEY"] = "73160309371293022383902397268374097245"

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db.init_app(app)
api.register_blueprint(TasksBlueprint)
api.register_blueprint(UserBlueprint)

with app.app_context():
    db.create_all()