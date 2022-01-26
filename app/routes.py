from flask import Blueprint, jsonify, request
from flask.json import jsonify
from app import db
from app.models.player import Player
from app.models.trip import Trip
from app.models.player_trip import PlayerTrip
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

players_bp = Blueprint("players", __name__, url_prefix="/players")
trips_bp = Blueprint("trips", __name__, url_prefix="/trips")
players_trips_bp = Blueprint("players_trips", __name__, url_prefix="/players_trips")


# PLAYERS ROUTES

@players_bp.route("", methods=['GET'], strict_slashes=False)
def get_players():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    players = Player.query.all()
    response = [player.to_dict() for player in players]

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

    new_player = Player(username=username, phone_number=phone)
    db.session.add(new_player)
    db.session.commit()
    return jsonify(f"{request_body['username']} successfully created"), 201

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

    db.session.commit()
    return jsonify(f"{player.username} successfully updated"), 200

# TRIPS ROUTES

@trips_bp.route("", methods=["POST"], strict_slashes=False)
def post_trip():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    new_trip = Trip(date=datetime.now())
    db.session.add(new_trip)
    db.session.commit()

    return jsonify("Trip successfully created"), 201

# PLAYERS X TRIPS ROUTES

@players_trips_bp.route("", methods=["POST"], strict_slashes=False)
def add_player_to_trip():
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    trip_id = request.args.get("trip_id")
    player_id = request.args.get('player_id')

    player = Player.query.get_or_404(player_id)
    trip = Trip.query.get_or_404(trip_id)

    player.trips.append(trip)
    db.session.commit()

    return jsonify(f"trip successfully added to {player.username}'s profile"), 200

