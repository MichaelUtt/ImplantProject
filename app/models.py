from sqlalchemy import ForeignKey

from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Report(db.Model):
    __tablename__ = "Report"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128))
    number = db.Column(db.String(32))
    doctor = db.Column(db.String(128))
    date = db.Column(db.Date)
    uncoverdate = db.Column(db.Date)
    restoredate = db.Column(db.Date)

    implant_id = db.Column(db.Integer, ForeignKey('implant.id'))
    implants = relationship("Implant")

    cap_id = db.Column(db.Integer, ForeignKey('caps.id'))
    caps = relationship("Caps")

    part_id = db.Column(db.Integer, ForeignKey('restorativeParts.id'))
    parts = relationship("RestorativeParts")

    details = db.Column(db.Text)
    restore = db.Column(db.Text)
    anesthetic = db.Column(db.Text)
    tolerance = db.Column(db.String(32))
    rx = db.Column(db.Text)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Implant(db.Model):
    __tablename__ = "implant"
    id = db.Column(db.Integer, primary_key=True)

    data = db.Column(db.Text, index=True, unique=True)

class Caps(db.Model):
    __tablename__ = "caps"
    id = db.Column(db.Integer, primary_key=True)

    data = db.Column(db.Text, index=True, unique=True)

class RestorativeParts(db.Model):
    __tablename__ = "restorativeParts"
    id = db.Column(db.Integer, primary_key=True)

    data = db.Column(db.Text, index=True, unique=True)



