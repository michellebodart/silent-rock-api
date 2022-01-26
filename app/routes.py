from flask import Blueprint, jsonify, request
from flask.json import jsonify
from app import db
from app.models.player import Player
from dotenv import load_dotenv
import os

load_dotenv()

players_bp = Blueprint("books", __name__, url_prefix="/players")

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
    error_msg = {}
    if Player.query.get(request_body['username']):
        error_msg["username"] = "Sorry, that username is taken"
    if Player.query.filter(Player.phone_number == request_body['phone']).first():
        error_msg["phone"] = "The phone number you entered is already registered with an account"
    if error_msg:
        return jsonify(error_msg), 400

    new_player = Player(username=request_body['username'], phone_number=request_body["phone"])
    db.session.add(new_player)
    db.session.commit()
    return jsonify(f"{request_body['username']} successfully created"), 201

@players_bp.route("<username>", methods=['GET'], strict_slashes=False)
def get_player(username):
    api_key = request.args.get('API_KEY')
    if api_key != os.environ.get("API_KEY"):
        return jsonify("Access denied"), 403

    player = Player.query.get_or_404(username)
    return jsonify(player.to_dict()), 200
    

