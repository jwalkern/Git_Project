from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from iotrace.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'accounts.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from iotrace.accounts.routes import accounts
    from iotrace.devices.routes import devices
    from iotrace.main.routes import main
    
    app.register_blueprint(accounts)
    app.register_blueprint(devices)
    app.register_blueprint(main)
    
    return app
    