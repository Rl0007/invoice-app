from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_login import LoginManager
from app.models import db, User, initialize_db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "blank"

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    from app.routes import api
    from app.auth import auth
    from app.views import views

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(views, url_prefix="/")
    initialize_db()
    return app
