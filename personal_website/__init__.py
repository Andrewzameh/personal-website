from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sZWt5zd6ReU2zRafUxzf3gGxk9E8Qmfj"

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
