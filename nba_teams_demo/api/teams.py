from sqlalchemy import exc

# Custom Packages Import
from nba_teams_demo.database import db
from nba_teams_demo.database.models import Team


def team_exists(team_id=None, team_name=None):
    if team_id:
        return Team.query.filter(Team.id == team_id).scalar()
    elif team_name:
        return Team.query.filter(Team.name == team_name).scalar()


def is_duplicate_team_name(team_id, team_name):
    return Team.query.filter(Team.name == team_name).filter(Team.id != team_id).scalar()


def get_all_teams():
    return Team.query.all()


def get_team(team_id=None, team_name=None):
    team = None
    if team_id:
        if team_exists(team_id=team_id):
            team = Team.query.filter(Team.id == team_id).one()
    elif team_name:
        if team_exists(team_name=team_name):
            team = Team.query.filter(Team.name == team_name).one()
    return team


def add_team(team_name):
    team = Team(team_name)
    try:
        db.session.add(team)
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        db.session().rollback()
        return False


def update_team(team_id, team_name):
    team = get_team(team_id=team_id)
    team.name = team_name
    try:
        db.session.add(team)
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        db.session().rollback()
        return False


def delete_team(team_id):
    team = get_team(team_id=team_id)
    try:
        db.session.delete(team)
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        db.session().rollback()
        return False
