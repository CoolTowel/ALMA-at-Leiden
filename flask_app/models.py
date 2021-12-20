from datetime import datetime
from flask import redirect, url_for, flash
from flask_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler  # In unauthorized_handler we have a callback URL
def unauthorized_callback():
    # In call back url we can specify where we want to
    flash('Please login first.', 'info')
    return redirect(url_for('login'))


user_antenna = db.Table(
    'user_antenna', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('antenna_id', db.ForeignKey('antenna.id'), primary_key=True))

user_picture = db.Table(
    'user_picture', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('picture_id', db.ForeignKey('picture.id'), primary_key=True))

user_question = db.Table(
    'user_question', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.ForeignKey('question.id'), primary_key=True))


# 为了避免不必要的bug，所有天线，用户，照片数据都以string存储和传输。即使是数字，也以string而非integer。
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    antennas = db.relationship('Antenna',
                               secondary=user_antenna,
                               back_populates='users')
    pictures = db.relationship('Picture',
                               secondary=user_picture,
                               back_populates='users')
    questions = db.relationship('Question',
                                secondary=user_question,
                                back_populates='users')

    def __repr__(self):
        return (self.username)


class Antenna(db.Model):
    __tablename__ = 'antenna'
    id = db.Column(db.Integer, primary_key=True)
    antenna_id = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    longitude = db.Column(db.String(120), unique=True, nullable=False)
    latitude = db.Column(db.String(120), unique=True, nullable=False)
    altitude = db.Column(db.String(120), nullable=False)
    users = db.relationship('User',
                            secondary=user_antenna,
                            back_populates='antennas')

    def __repr__(self):
        return (self.id)


class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    path = db.Column(db.String(120), nullable=False)
    users = db.relationship('User',
                            secondary=user_picture,
                            back_populates='pictures')

    def __repr__(self):
        return (self.id)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship('User',
                            secondary=user_question,
                            back_populates='questions')
    def __repr__(self):
        return (self.id)