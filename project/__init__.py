from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from json import load

# Initialise database for storing of user data
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Set config which includes SECRET_KEY and SQLALCHEMY_DaTABASE_URI
    app.config.from_file("config.json", load=load)

    db.init_app(app)

    # Setup Login Manager to manage sessions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    # Set User Loader - used to query who the login user is to check
    # whether can login or not
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for authentication
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()
        
    return app


