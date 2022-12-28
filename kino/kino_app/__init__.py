from flask import Flask
from flask_login import LoginManager
from kino_app.routes.auth import User

login_manager = LoginManager()
visit_count = dict()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from kino_app.routes.main_route import main
    app.register_blueprint(main, url_prefix='/')
    from kino_app.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User().load_from_db(user_id)

    return app
