from app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profilepicture = db.Column(db.String(120), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    #relationships
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    resources = db.relationship('Resource', backref='uploader', lazy='dynamic')
    profile = db.relationship('Profile', uselist=False, backref='user')
    Notifications = db.relationship('Notification', backref='user', lazy='dynamic')


    def __repr__(self):
        return f'<User {self.username}>'
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Message {self.body[:20]}>'
    
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Resource {self.title}>'
        

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    website = db.Column(db.String(100))
    social_links = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Profile of User ID {self.user_id}>'
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Notification {self.message[:20]}>'

class StudyGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    users = db.relationship('User', secondary='study_group_users', backref='study_groups')

    def __repr__(self):
        return f'<StudyGroup {self.name}>'

study_group_user = db.Table('study_group_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('study_group_id', db.Integer, db.ForeignKey('study_group.id'), primary_key=True)
)