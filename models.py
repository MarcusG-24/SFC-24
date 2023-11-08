from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class Students(db.Model, UserMixin):
    studID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    gender = db.Column(db.String(1))
    team = db.Column(db.String(2))
    house = db.Column(db.String(15))
    grade = db.Column(db.Integer)
    yearBorn = db.Column(db.Integer)
    activity = db.Column(db.String(35))


class Houses(db.Model, UserMixin):
    team = db.Column(db.String(2), primary_key=True)
    house = db.Column(db.String(12))
    bgcolor = db.Column(db.String(22))


class Activities(db.Model, UserMixin):
    act_Code = db.Column(db.String(3), primary_key=True)
    act_Name = db.Column(db.String(26))
    min = db.Column((db.Integer))


class Entries(db.Model, UserMixin):
    entryID = db.Column((db.Integer), primary_key=True, autoincrement=True)
    act_Code = db.Column(db.String(3))
    act_Name = db.Column(db.String(26))
    studID = db.Column(db.Integer)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    team = db.Column(db.String(2))
    grade = db.Column(db.Integer)
    gender = db.Column(db.String(1))

