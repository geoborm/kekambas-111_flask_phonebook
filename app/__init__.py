from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create an instance of the LoginManager to set up Authentication
login = LoginManager(app)
# Tell the login manager where to redirect if a user is not logged in
login.login_view = 'login'
# login.login_message = "Hey you can't do that!"
login.login_message_category = 'danger'

from app import routes, models
