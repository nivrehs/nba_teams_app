from datetime import datetime
from nba_teams_demo.database import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_dt = db.Column(db.DateTime)

    def __init__(self, name, created_dt=None):
        self.name = name
        if created_dt is None:
            created_dt = datetime.utcnow()
        self.created_dt = created_dt

    def __repr__(self):
        return '<Team %r>' % self.name

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_dt = db.Column(db.DateTime)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', backref=db.backref('player', lazy='dynamic'))

    def __init__(self, name, team, created_dt=None):
        self.name = name
        if created_dt is None:
            created_dt = datetime.utcnow()
        self.created_dt = created_dt
        self.team = team

    def __repr__(self):
        return '<Player %r>' % self.name