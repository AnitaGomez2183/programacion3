from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    with app.app_context():
        from .auth import auth as auth_blueprint

        app.register_blueprint(auth_blueprint)

        from .routes import main as main_blueprint

        app.register_blueprint(main_blueprint)

        from sqlalchemy import text
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            stmt = text(
                "SELECT user_id, username, email FROM view_users WHERE user_id = :user_id"
            )
            result = db.session.execute(stmt, {"user_id": user_id}).fetchone()

            if result:
                return User(
                    user_id=result[0],
                    username=result[1],
                    email=result[2],
                    password=None,
                )
            return None

    return app
