from app import routes, db, models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import config


app = Flask(__name__)
app.config.from_object(config.Config())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()
