from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'pacjenci.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.pacjenci.routes import pacjenci
    from flaskblog.wizyty.routes import wizyty
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(pacjenci)
    app.register_blueprint(wizyty)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
