import json

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_NAME = "database.db"

with open("/mnt/sdb3/Code/Projects/personal-website/config.json") as f:
    config = json.load(f)

SECRET_KEY = config["SECRET_KEY"]


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .aiemail import aiemail
    from .auth import auth
    from .models import User
    from .views import views

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(aiemail, url_prefix="/")

    return app
