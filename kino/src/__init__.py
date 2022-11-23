from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from src.routes.main_route import main
    app.register_blueprint(main, url_prefix='/')
    from src.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app
