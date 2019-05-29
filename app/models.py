from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# class TaskList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.column(db.String(100))
#     tasks = db.relationship('Task', backref='tasklist', lazy='dynamic')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # tasklist_id = db.Column(db.Integer, db.ForeignKey('tasklist.id'))

    def __repr__(self):
        return '<Task {}>'.format(self.body)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
