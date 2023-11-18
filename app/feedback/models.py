from datetime import datetime
from app import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    feedback = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))