from app import db, login_manager
from flask_login import UserMixin
from app.models.event import Event
from app.models.comment import Comment
from app.models.ticket import Ticket

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    events = db.relationship('Event', backref='creator', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    tickets = db.relationship('Ticket', backref='buyer', lazy=True)
