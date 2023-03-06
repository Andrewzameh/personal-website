from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    notes = db.relationship("Note")
    aiEmails = db.relationship("AiEmail")


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class AiEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userPrompt = db.Column(db.String(10000))
    initPrompt = db.Column(db.NVARCHAR(20000))
    style = db.Column(db.String(32))
    output = db.Column(db.String(32000))
    tokens = db.Column(db.Integer)
    model = db.Column(db.String(32))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
