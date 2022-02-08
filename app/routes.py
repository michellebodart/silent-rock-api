from email import message
from flask import Blueprint, jsonify, request
from flask.json import jsonify
from sqlalchemy import true
from app import db
from app.models.player import Player
from app.models.trip import Trip
from app.models.player_trip import PlayerTrip
from app.models.pending_player_trip import PendingPlayerTrip
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

players_bp = Blueprint("players", __name__, url_prefix="/players")
trips_bp = Blueprint("trips", __name__, url_prefix="/trips")
players_trips_bp = Blueprint("players_trips", __name__, url_prefix="/players_trips")
pending_players_trips_bp = Blueprint("pending_players_trips", __name__, url_prefix="/pending_players_trips")


# PLAYERS ROUTES

@players_bp.route("", methods=['GET'], strict_slashes=False)
def get_players():
    api_key = request.args.get('API_KEY')
    sort_basis = request.args.get('sort_basis')
    filter_criteria = request.args.get('filter_criteria')

    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    players = Player.query.all()

    response = [player.to_dict() for player in players]

    if sort_basis == "username":
        response = sorted(response, key = lambda i: i['username'].lower())
    
    elif sort_basis == "trips":
        response = sorted(response, key = lambda i: len(i['trips']), reverse=True)

        if filter_criteria != "all":
            def filter_function(trip):
                if trip["season"] == filter_criteria:
                    return True
                else:
                    return False
            response = sorted(response, key = lambda i: len(list(filter(filter_function, i['trips']))), reverse=True)

    return jsonify(response), 200

@players_bp.route("", methods=['POST'], strict_slashes=False)
def add_player():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    request_body = request.get_json()
    phone = request_body['phone']
    username = request_body['username']
    error_msg = {}
    if Player.query.filter(Player.username == username).first():
        error_msg["username"] = "Sorry, that username is taken"
    if Player.query.filter(Player.phone_number == phone).first():
        error_msg["phone"] = "The phone number you entered is already registered with an account"
    if error_msg:
        return jsonify(error_msg), 400

    new_player = Player(username=username, phone_number=phone, visible_on_leaderboard=True)
    db.session.add(new_player)
    db.session.commit()
    response = {
        "id": Player.query.filter(Player.username == username).first().id,
        "message": f"{username} successfully created"
    }
    return jsonify(response), 201

@players_bp.route("<id>", methods=['GET'], strict_slashes=False)
def get_player(id):
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    player = Player.query.get_or_404(id)
    return jsonify(player.to_dict()), 200
    
@players_bp.route("<player_id>", methods=['PATCH'], strict_slashes=False)
def update_player(player_id):
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    player = Player.query.get_or_404(player_id)
    
    request_body = request.get_json()
    username = request_body.get('username')
    phone = request_body.get('phone')
    visible_on_leaderboard = request_body.get('visible_on_leaderboard')
    error_msg = {}
    if Player.query.filter(Player.username == username).first():
        error_msg["username"] = "Sorry, that username is taken"
    if Player.query.filter(Player.phone_number == phone).first():
        error_msg["phone"] = "The phone number you entered is already registered with an account"
    if error_msg:
        return jsonify(error_msg), 400

    if username:
        player.username = username

    if phone:
        player.phone_number = phone

    if visible_on_leaderboard != None:
        player.visible_on_leaderboard = visible_on_leaderboard

    db.session.commit()
    return jsonify(f"{player.username} successfully updated"), 200

@players_bp.route("<player_id>", methods=['DELETE'], strict_slashes=False)
def delete_player(player_id):
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    player = Player.query.get_or_404(player_id)
    username = player.username
    db.session.delete(player)
    db.session.commit()
    return jsonify(f"{username} successfully deleted"), 200

# TRIPS ROUTES

@trips_bp.route("", methods=["POST"], strict_slashes=False)
def post_trip():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    new_trip = Trip(date=datetime.now())
    db.session.add(new_trip)
    db.session.commit()

    response = {
        "message": "Trip successfully create",
        "trip_id": new_trip.id
    }

    return jsonify(response), 201

# PLAYERS X TRIPS ROUTES

@players_trips_bp.route("", methods=["POST"], strict_slashes=False)
def add_player_to_trip():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    request_body = request.get_json()
    trip_id = request_body["trip_id"]
    player_ids = request_body["player_ids"]
    trip = Trip.query.get_or_404(trip_id)
    player_usernames = []
    for player_id in player_ids:
        player = Player.query.get_or_404(player_id)
        player.trips.append(trip)
        db.session.commit()
        player_usernames.append(player.username)

    db.session.commit()

    players_string = ""
    for player_username in player_usernames:
        players_string += player_username + ", "
    return jsonify(f"trip successfully added to {players_string[:-2]}'s profile(s)"), 200

# PENDING PLAYERS X TRIPS 

@pending_players_trips_bp.route("", methods=["POST"], strict_slashes=False)
def add_player_to_pending_trip():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    request_body = request.get_json()
    trip_id = request_body["trip_id"]
    player_ids = request_body["player_ids"]
    trip = Trip.query.get_or_404(trip_id)
    player_usernames = []
    for player_id in player_ids:
        player = Player.query.get_or_404(player_id)
        player.pending_trips.append(trip)
        db.session.commit()
        player_usernames.append(player.username)

    db.session.commit()

    players_string = ""
    for player_username in player_usernames:
        players_string += player_username + ", "
    return jsonify(f"trip successfully added to {players_string[:-2]}'s pending trips"), 200

@pending_players_trips_bp.route("", methods=["DELETE"], strict_slashes=False)
def delete_pending_trip():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    request_body = request.get_json()
    trip_id = request_body["trip_id"]
    player_ids = request_body["player_ids"]
    accept = request_body["accept"]
    trip = Trip.query.get_or_404(trip_id)
    player_usernames = []
    for player_id in player_ids:
        player = Player.query.get_or_404(player_id)
        connection = PendingPlayerTrip.query.filter(PendingPlayerTrip.player_id == player.id, PendingPlayerTrip.trip_id == trip.id).first()
        if connection == None:
            return "pending trip not found", 404
        if accept:
            player.trips.append(trip)
        player.pending_trips.remove(trip)
        db.session.commit()
        player_usernames.append(player.username)

    db.session.commit()

    players_string = ""
    for player_username in player_usernames:
        players_string += player_username + ", "
    players_string = players_string[:-2] + "'s pending trips"
    if accept:
        players_string += " and added to their profile(s)"
    return jsonify(f"trip successfully deleted from {players_string}"), 200
