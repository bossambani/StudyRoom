from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
db_Name = "app.db"
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_Name}'

    #Email configuration 
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'bossambaka@gmail.com'
    app.config['MAIL_PASSWORD'] = 'aehp nucu zoan evkc'
    app.config['MAIL_DEFAULT_SENDER'] = 'bossambaka@gmail.com'

    mail.init_app(app)
    db.init_app(app)


    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    
    # Register blueprints
    from app.views import views
    from app.auth import auth
    from app.study_room import study_room
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(study_room, url_prefix='/study_room')
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models import User, Profile, StudyRoom, Resource, Notification, Message, StudyRoomMembers
    
    # Create database if it doesn't exist
    create_database(app)
    
    # Set up login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    # Ensure the directory exists or adjust the path as needed
    if not os.path.exists('app/' + db_Name):
        with app.app_context():
            db.create_all()
            
