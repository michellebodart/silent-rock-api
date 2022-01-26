import pytest
from app import create_app
from app import db
from app.models.player import Player
from app.models.trip import Trip
from datetime import datetime


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_players_no_trips(app):
    # Arrange
    player1 = Player(username="michellebodart", phone_number="+1 (503) 707-9796")
    player2 = Player(username="reneebodart", phone_number="+1 (503) 707-9797")
    db.session.add_all([player1, player2])
    db.session.commit()

@pytest.fixture
def two_players_one_trip(app):
    # Arrange
    player1 = Player(username="michellebodart", phone_number="+1 (503) 707-9796")
    player2 = Player(username="reneebodart", phone_number="+1 (503) 707-9797")


    trip = Trip(date='Wed Jan 26 11:25:57 2022')

    db.session.add_all([player1, player2, trip])
    db.session.commit()

    michelle = Player.query.get(1)
    trip = Trip.query.get(1)
    michelle.trips.append(trip)
    db.session.commit()