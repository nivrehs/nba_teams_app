from sqlalchemy import exc

# Custom Packages Import
from nba_teams_demo.database import db
from nba_teams_demo.database.models import Player
from nba_teams_demo.api.Constants import Constants
from nba_teams_demo.api.teams import get_all_teams, get_team


def player_exists(player_id=None, player_name=None):
    if player_id:
        return Player.query.filter(Player.id == player_id).scalar()
    elif player_name:
        return Player.query.filter(Player.name == player_name).scalar()


def is_duplicate_player_name(player_id, player_name):
    return Player.query.filter(Player.name == player_name).filter(Player.id != player_id).scalar()


def get_player(player_id):
    if player_exists(player_id=player_id):
        return Player.query.filter(Player.id == player_id).one()
    return False


def get_all_players(team=None):
    response = []
    if team:
        players = Player.query.filter(Player.team == team).all()
        if players:
            for player in players:
                response.append({"player_id": player.id,
                                 "player_name": player.name})
    else:
        teams = {}
        team_list = get_all_teams()
        players = Player.query.all()

        if players:
            for team in team_list:
                teams[team.id] = team.name

            for player in players:
                response.append({"player_id": player.id,
                                 "player_name": player.name,
                                 "team_name": teams[player.team_id],
                                 "team_id": player.team_id})
    return response


def add_player(player_name, team):
    player = Player(player_name, team)
    try:
        db.session.add(player)
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        db.session().rollback()
        return False


def update_player(player_id, player_name, team_id):
    player = get_player(player_id=player_id)
    if player_name:
        player.name = player_name
    if team_id:
        player.team_id = team_id
    try:
        db.session.add(player)
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        db.session().rollback()
        return False


def delete_player(player_id):
    player = Player.query.filter(Player.id == player_id).one()
    try:
        db.session.delete(player)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session().rollback()
        return False
    return True


def get_free_agents():
    team = get_team(team_name=Constants.FREE_AGENTS)
    response = []
    if team:
        players = Player.query.filter(Player.team == team).all()
        if players:
            for player in players:
                response.append({"player_id": player.id, "player_name": player.name})
    return response
