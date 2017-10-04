from flask import Blueprint, request
from sqlalchemy import exc
import ujson

# Custom Packages Import
from nba_teams_demo.database import db
from nba_teams_demo.database.models import Team, Player

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return (ujson.dumps({'message': 'This is the homepage for the NBA teams api!'}), 200)


@api.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    response = []
    if teams:
        for team in teams:
            response.append({"id": team.id, "name": team.name})
    return (ujson.dumps({"teams": response}), 200)


@api.route('/team', methods=['POST'])
def add_team():
    team_name = request.values.get("team_name", "")
    status = "Failed"
    http_code = 400

    if team_name:
        team_name_exists = Team.query.filter_by(name=team_name).scalar() is not None
        if team_name_exists:
            description = "Team %s is already in the database" % team_name
            http_code = 409
        else:
            team = Team(team_name)
            try:
                db.session.add(team)
                db.session.commit()
                status = "Success"
                description = "Successfully added %s team" % team_name
                http_code = 201
            except exc.SQLAlchemyError as e:
                db.session().rollback()
                description = "Team %s was not created due to an error." % team_name
    else:
        description = "Team name not provided"

    response = {
        "status": status,
        "description": description
    }
    return (ujson.dumps(response), http_code)


@api.route('/team/<int:id>', methods=['PUT'])
def update_team(id):
    team_name = request.values.get("team_name", "")
    status = "Failed"
    http_code = 400

    if team_name:
        # check if team id is valid
        team_id_exists = Team.query.filter(Team.id == id).scalar() is not None
        if team_id_exists:
            # check if team name is already existing in the database
            is_duplicate_team_name = Team.query.filter(Team.name == team_name). \
                                         filter(Team.id != id).scalar() is not None
            if is_duplicate_team_name:
                description = "Team name %s is already in the database" % team_name
                http_code = 409
            else:
                team = Team.query.filter(Team.id == id).one()
                team.name = team_name
                try:
                    db.session.add(team)
                    db.session.commit()
                    status = "Success"
                    description = "Successfully updated team %s" % id
                    http_code = 204
                except exc.SQLAlchemyError as e:
                    db.session().rollback()
                    description = "Team %s was not updated due to an error." % id
        else:
            description = "Invalid team id."
    else:
        description = "Team name not supplied."

    response = {
        "status": status,
        "description": description
    }
    return (ujson.dumps(response), http_code)


@api.route('/team/<int:id>', methods=['DELETE'])
def delete_team(id):
    status = "Success"
    description = "Successfully deleted team %s" % id
    http_code = 204

    team_id_exists = Team.query.filter(Team.id == id).scalar() is not None
    if team_id_exists:
        team = Team.query.filter(Team.id == id).one()
        try:
            db.session.delete(team)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session().rollback()
            status = "Failed"
            description = "Team %s was not deleted due to an error." % id
            http_code = 400

    response = {
        "status": status,
        "description": description
    }
    return (ujson.dumps(response), http_code)


@api.route('/team/<int:id>/roster', methods=['GET'])
def get_team_roster(id):
    is_team_valid = Team.query.filter(Team.id == id).scalar() is not None
    if is_team_valid:
        team = Team.query.filter(Team.id == id).one()
        players = Player.query.filter(Player.team == team).all()
        response = []

        if players:
            for player in players:
                response.append({"player_id": player.id, "player_name": player.name})
        return (ujson.dumps({"%s players" % team.name: response}), 200)
    else:
        response = {
            "status": "Failed",
            "description": "Invalid Team id"
        }
        return (ujson.dumps(response), 400)


@api.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    response = []

    if players:
        teams = {}
        team_list = Team.query.all()
        for team in team_list:
            teams[team.id] = team.name

        for player in players:
            response.append({"player_id": player.id, "player_name": player.name, "team_name": teams[player.team_id],
                             "team_id": player.team_id})
    return (ujson.dumps({"players": response}), 200)


@api.route('/player', methods=['POST'])
def add_player():
    player_name = request.values.get("player_name", "")
    team_id = request.values.get("team_id", "")
    status = "Failed"
    http_code = 400

    if player_name:
        if team_id:
            player_exists = Player.query.filter_by(name=player_name).scalar() is not None
            if player_exists:
                description = "Player %s is already in the database" % player_name
                http_code = 409
            else:
                team_exists = Team.query.filter(Team.id == team_id).scalar() is not None
                if team_exists:
                    team = Team.query.filter(Team.id == team_id).one()
                    player = Player(player_name, team)
                    try:
                        db.session.add(player)
                        db.session.commit()
                        status = "Success",
                        description = "Successfully added %s to %s" % (player_name, team.name)
                        http_code = 201
                    except exc.SQLAlchemyError as e:
                        db.session().rollback()
                        description = "Player %s was not added due to an error." % player_name
                else:
                    description = "Invalid Team id"
        else:
            description = "Team id not provided"
    else:
        description = "Player name not provided"

    response = {
        "status": status,
        "description": description
    }
    return (ujson.dumps(response), http_code)


@api.route('/player/<int:id>', methods=['PUT'])
def update_player(id):
    player_name = request.values.get("player_name", "")
    team_id = request.values.get("team_id", "")
    status = "Failed"
    http_code = 400

    # check if player id supplied is valid
    player_exists = Player.query.filter(Player.id == id).scalar() is not None
    if player_exists:
        # check if there's anything to update
        if player_name or team_id:
            if player_name:
                # check if player name is already in the database
                is_duplicate_player_name = Player.query.filter(Player.name == player_name). \
                                               filter(Player.id != id).scalar() is not None
                if is_duplicate_player_name:
                    response = {
                        "status": status,
                        "description": "Player name %s is already in the database" % player_name
                    }
                    return (ujson.dumps(response), 409)

            if team_id:
                # check if Team id provided is valid
                is_team_valid = Team.query.filter(Team.id == team_id).scalar() is not None
                if not is_team_valid:
                    response = {
                        "status": status,
                        "description": "Invalid Team id"
                    }
                    return (ujson.dumps(response), http_code)

                team = Team.query.filter(Team.id == team_id).one()

            player = Player.query.filter(Player.id == id).one()
            if player_name:
                player.name = player_name
            if team_id:
                player.team = team
            try:
                db.session.add(player)
                db.session.commit()
                status = "Success",
                description = "Successfully updated %s" % (player_name)
                http_code = 201
            except exc.SQLAlchemyError as e:
                db.session().rollback()
                description = "Player %s was not updated due to an error." % player_name
        else:
            description = "Nothing to update"
    else:
        description = "Invalid Player id"

    response = {
        "status": status,
        "description": description
    }
    return (ujson.dumps(response), http_code)


@api.route('/player/<int:id>', methods=['DELETE'])
def delete_player(id):
    status = "Success"
    description = "Successfully deleted player id %s" % id
    http_code = 204

    # only execute delete if player id provided is valid
    is_player_id_valid = Player.query.filter(Player.id == id).scalar() is not None
    if is_player_id_valid:
        player = Player.query.filter(Player.id == id).one()
        try:
            db.session.delete(player)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session().rollback()
            status = "Failed"
            description = "Player id %s was not deleted due to an error." % id
            http_code = 400

    response = {
        "status": status,
        "description": description
    }
    return (ujson.dumps(response), http_code)


@api.route('/players/free_agent', methods=['GET'])
def get_free_agents():
    team = Team.query.filter_by(name='Free Agents').one()
    players = Player.query.filter(Player.team == team).all()
    response = []

    if players:
        for player in players:
            response.append({"player_id": player.id, "player_name": player.name})
    return (ujson.dumps({"players": response}), 200)