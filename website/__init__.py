from mailbox import Message
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import pytz
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah_k_jshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/tubitak2'


    
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.context_processor
    def inject_user():
        return {'user': current_user}
    




    # Register the custom datetimeformat filter
    def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
        local_timezone = pytz.timezone('Europe/Istanbul')  # Replace with your local timezone
        value = value.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        return value.strftime(format)

    app.jinja_env.filters['datetimeformat'] = datetimeformat

    return app