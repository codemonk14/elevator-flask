from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Elevator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(db.String(1), unique=True, nullable=False)
    current_floor = db.Column(db.Integer, default=0)
    people_count = db.Column(db.Integer, default=0)
    direction = db.Column(db.String(1), default='-')

class UserRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_floor = db.Column(db.Integer, nullable=False)
    destination_floor = db.Column(db.Integer, nullable=False)
    elevator_id = db.Column(db.String(1), db.ForeignKey('elevator.elevator_id'))
    people_count = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
