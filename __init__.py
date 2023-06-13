from flask import Flask

SECRET_KEY = 'asdfasdf4q89w0f4q4fasdfasda3c'


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    from .ai import ai
    from .chain import chain

    app.register_blueprint(chain, url_prefix="/")
    app.register_blueprint(ai, url_prefix="/")

    return app
