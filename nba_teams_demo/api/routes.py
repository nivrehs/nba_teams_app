from flask import Blueprint, request
import ujson

# Custom Packages Import
from nba_teams_demo.api.teams import add_team, delete_team, get_all_teams, get_team, update_team
from nba_teams_demo.api.teams import is_duplicate_team_name, team_exists
from nba_teams_demo.api.players import get_all_players, get_free_agents, get_player
from nba_teams_demo.api.players import add_player, delete_player, update_player
from nba_teams_demo.api.players import is_duplicate_player_name, player_exists
from nba_teams_demo.api.Constants import Constants

api = Blueprint('api', __name__)


@api.route('/')
def index():
    return ujson.dumps({'message': 'This is the homepage for the NBA teams api!'}), 200


@api.route('/teams', methods=['GET', 'POST'])
def teams():
    if request.method == 'GET':
        teams = get_all_teams()
        response = []
        if teams:
            for team in teams:
                response.append({"team_id": team.id, "team_name": team.name})
        return ujson.dumps({"teams": response}), 200
    elif request.method == 'POST':
        team_name = request.values.get("team_name", "")
        if team_name:
            if team_exists(team_name=team_name):
                result = Constants.DUPLICATE_TEAM_NAME
            else:
                add_result = add_team(team_name)
                if add_result:
                    result = Constants.CREATE_TEAM_SUCCESS
                else:
                    result = Constants.CREATE_TEAM_FAILED
        else:
            result = Constants.TEAM_NAME_NOT_PROVIDED

        return ujson.dumps(result['response']), result['http_code']


@api.route('/teams/<int:team_id>', methods=['DELETE', 'GET', 'PUT'])
def modify_teams(team_id):
    if request.method == 'PUT':
        team_name = request.values.get("team_name", "")
        # check if team id is valid
        if team_exists(team_id=team_id):
            if team_name:
                # check if team name is already existing in the database
                if is_duplicate_team_name(team_id, team_name):
                    result = Constants.DUPLICATE_TEAM_NAME
                else:
                    update_result = update_team(team_id, team_name)
                    if update_result:
                        result = Constants.UPDATE_TEAM_SUCCESS
                    else:
                        result = Constants.UPDATE_TEAM_SUCCESS
            else:
                result = Constants.NOTHING_TO_UPDATE
        else:
            result = Constants.INVALID_TEAM_ID
        return ujson.dumps(result['response']), result['http_code']
    elif request.method == 'DELETE':
        result = Constants.DELETE_TEAM_SUCCESS
        if team_exists(team_id=team_id):
            delete_result = delete_team(team_id)
            if delete_result is None:
                result = Constants.DELETE_TEAM_FAILED
        return ujson.dumps(result['response']), result['http_code']
    elif request.method == 'GET':
        team = get_team(team_id=team_id)
        if team:
            response = {"team_id": team.id, "team_name": team.name}
            return ujson.dumps(response), 200

        result = Constants.TEAM_NOT_FOUND
        return ujson.dumps(result['response']), result['http_code']


@api.route('/teams/<int:team_id>/players', methods=['GET'])
def get(team_id):
    if team_exists(team_id=team_id):
        team = get_team(team_id=team_id)
        players = get_all_players(team)
        response = {'team': team.name, 'players': players}
        return ujson.dumps(response), 200
    else:
        result = Constants.INVALID_TEAM_ID
        return ujson.dumps(result['response']), result['http_code']


@api.route('/players', methods=['GET', 'POST'])
def players():
    if request.method == 'GET':
        return ujson.dumps({"players": get_all_players()}), 200
    elif request.method == 'POST':
        player_name = request.values.get("player_name", "")
        team_id = request.values.get("team_id", "")

        if player_name:
            if team_id:
                if player_exists(player_name=player_name):
                    result = Constants.DUPLICATE_PLAYER_NAME
                else:
                    if team_exists(team_id=team_id):
                        add_result = add_player(player_name, get_team(team_id=team_id))
                        if add_result:
                            result = Constants.CREATE_PLAYER_SUCCESS
                        else:
                            result = Constants.CREATE_PLAYER_FAILED
                    else:
                        result = Constants.INVALID_TEAM_ID
            else:
                result = Constants.MISSING_TEAM_ID
        else:
            result = Constants.MISSING_PLAYER_NAME
        return ujson.dumps(result['response']), result['http_code']


@api.route('/players/<int:player_id>', methods=['DELETE', 'GET', 'PUT'])
def modify_players(player_id):
    if request.method == 'PUT':
        player_name = request.values.get("player_name", "")
        team_id = request.values.get("team_id", "")

        if player_exists(player_id=player_id):
            if player_name:
                # check if player name is already in the database
                if is_duplicate_player_name(player_id, player_name):
                    result = Constants.DUPLICATE_PLAYER_NAME
                    player_name = None
            if team_id:
                # check if Team id provided is valid
                if not team_exists(team_id=team_id):
                    result = Constants.INVALID_TEAM_ID
                    team_id = None

            if player_name or team_id:
                update_result = update_player(player_id, player_name, team_id)
                if update_result:
                    result = Constants.UPDATE_PLAYER_SUCCESS
                else:
                    result = Constants.UPDATE_PLAYER_FAILED
            else:
                result = Constants.NOTHING_TO_UPDATE
        else:
            result = Constants.PLAYER_NOT_FOUND
        return ujson.dumps(result['response']), result['http_code']
    elif request.method == 'DELETE':
        result = Constants.DELETE_PLAYER_SUCCESS
        # only execute delete if player id provided is valid
        if player_exists(player_id=player_id):
            delete_result = delete_player(player_id)
            if not delete_result:
                result = Constants.DELETE_PLAYER_FAILED
        return ujson.dumps(result['response']), result['http_code']
    elif request.method == 'GET':
        player = get_player(player_id)
        if player:
            team = get_team(team_id=player.team_id)
            response = {"player_id": player.id,
                        "player_name": player.name,
                        "team_id": player.team_id,
                        "team_name": team.name}
            return ujson.dumps(response), 200

        result = Constants.PLAYER_NOT_FOUND
        return ujson.dumps(result['response']), result['http_code']


@api.route('/players/free_agent', methods=['GET'])
def free_agents():
    result = get_free_agents()
    return ujson.dumps({"Free Agents": result}), 200
