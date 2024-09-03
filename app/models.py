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
    profilepicture = db.Column(db.String(120), nullable=True, default='default.jpg')
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    #relationships
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    resources = db.relationship('Resource', backref='uploader', lazy='dynamic')
    profile = db.relationship('Profile', uselist=False, backref='user')
    Notifications = db.relationship('Notification', backref='user', lazy='dynamic')


    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.profilepicture}>'
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Message {self.body[:20]}>'
    
class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'), nullable=False)

   
    room = db.relationship('StudyRoom', backref='resources')
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
    
class StudyRoomMembers(db.Model):
    __tablename__ = 'study_room_members'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    study_room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudyRoom(db.Model):
    __tablename__ = 'study_room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    members = db.relationship('User', secondary='study_room_members', backref='study_rooms')
    def __repr__(self):
        return f'<StudyGroup {self.name}>'

