import pytest
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("API_KEY")

# GET /players endpoint

def test_access_denied_if_wrong_api_key(client):
    # Act
    response = client.get(f'/players?API_KEY=wrong_key')

    # Assert
    assert response.status_code == 403


def test_get_players_no_players(client):
    # Act
    response = client.get(f'/players?API_KEY={API_KEY}')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_players_no_routes(client, two_players_no_trips):
    # Act
    response = client.get(f'/players?API_KEY={API_KEY}')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "username": "michellebodart", 
        "phone": "+1 (503) 707-9796",
        "trips": []
        },
        {
        "id": 2,
        "username": "reneebodart", 
        "phone": "+1 (503) 707-9797",
        "trips": []
        }]

def test_get_players_with_trips(client, two_players_one_trip):
    # Act
    response = client.get(f'/players?API_KEY={API_KEY}')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "username": "michellebodart", 
        "phone": "+1 (503) 707-9796",
        "trips": [{
            "id": 1,
            "date": 'Wed, 26 Jan 2022 11:25:57 GMT',
            "season": "2021-2022"
        }]
        },
        {
        "id": 2,
        "username": "reneebodart", 
        "phone": "+1 (503) 707-9797",
        "trips": []
        }]

# POST /players endpoint

def test_access_denied_if_wrong_api_key(client):
    # Act
    response = client.post(f'/players?API_KEY=wrong_key')

    # Assert
    assert response.status_code == 403

def test_post_player_no_players(client):
    # Act
    request_body = {
        "username": "michellebodart",
        "phone": "+1 (503) 707-9796"
    }
    response = client.post(f'/players?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {'id': 1, 'message': 'michellebodart successfully created'}

def test_post_player_username_taken(client, two_players_no_trips):
    # Act
    request_body = {
        "username": "michellebodart",
        "phone": "+1 (503) 531-8286"
    }
    response = client.post(f'/players?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "username": "Sorry, that username is taken"
    }

def test_post_player_phone_taken(client, two_players_no_trips):
    # Act
    request_body = {
        "username": "teresabodart",
        "phone": "+1 (503) 707-9796"
    }
    response = client.post(f'/players?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "phone": "The phone number you entered is already registered with an account"
    }

def test_post_player_duplicate(client, two_players_no_trips):
    # Act
    request_body = {
        "username": "michellebodart",
        "phone": "+1 (503) 707-9796"
    }
    response = client.post(f'/players?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "phone": "The phone number you entered is already registered with an account",
        "username": "Sorry, that username is taken"
    }

# GET /players/<player_id> endpoint

def test_access_denied_if_wrong_api_key(client):
    # Act
    response = client.get(f'/players/1?API_KEY=wrong_key')

    # Assert
    assert response.status_code == 403

def test_404_if_player_doesnt_exist(client):
    # Act
    response = client.get(f'/players/1?API_KEY={API_KEY}')

    # Assert
    assert response.status_code == 404


def test_get_player_no_player(client):
    # Act
    response = client.get(f'/players/1?API_KEY={API_KEY}')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None

def test_get_player_with_trip(client, two_players_one_trip):
    # Act
    response = client.get(f'/players/1?API_KEY={API_KEY}')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "username": "michellebodart", 
        "phone": "+1 (503) 707-9796",
        "trips": [{
            "id": 1,
            "date": 'Wed, 26 Jan 2022 11:25:57 GMT',
            "season": "2021-2022"
        }]
        }

def test_get_player_without_trip(client, two_players_one_trip):
    # Act
    response = client.get(f'/players/2?API_KEY={API_KEY}')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "username": "reneebodart", 
        "phone": "+1 (503) 707-9797",
        "trips": []
        }

# PATCH /players/<username> endpoint

def test_access_denied_if_wrong_api_key(client):
    # Act
    response = client.patch(f'/players/1?API_KEY=wrong_key')

    # Assert
    assert response.status_code == 403

def test_404_if_player_doesnt_exist(client):
    # Act
    response = client.patch(f'/players/1?API_KEY={API_KEY}')

    # Assert
    assert response.status_code == 404

def test_update_player_username_one_trip(client, two_players_one_trip):
    # Act
    request_body = {
        "username": "mbodart"
    }
    response = client.patch(f'/players/1?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    all_players = client.get(f'/players?API_KEY={API_KEY}').get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "mbodart successfully updated"
    assert {
        "id": 1,
        "username": "mbodart",
        "phone": "+1 (503) 707-9796", 
        "trips": [{
            "id": 1,
            "date": 'Wed, 26 Jan 2022 11:25:57 GMT',
            "season": "2021-2022"
        }]
    } in all_players

def test_update_player_phone_one_trip(client, two_players_one_trip):
    # Act
    request_body = {
        "phone": "+1 (503) 531-8286"
    }
    response = client.patch(f'/players/1?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    all_players = client.get(f'/players?API_KEY={API_KEY}').get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "michellebodart successfully updated"
    assert {
        "id": 1,
        "username": "michellebodart",
        "phone": "+1 (503) 531-8286", 
        "trips": [{
            "id": 1,
            "date": 'Wed, 26 Jan 2022 11:25:57 GMT',
            "season": "2021-2022"
        }]
    } in all_players

def test_update_player_one_trip(client, two_players_one_trip):
    # Act
    request_body = {
        "phone": "+1 (503) 531-8286",
        "username": "mbodart"
    }
    response = client.patch(f'/players/1?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    all_players = client.get(f'/players?API_KEY={API_KEY}').get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "mbodart successfully updated"
    assert {
        "id": 1,
        "username": "mbodart",
        "phone": "+1 (503) 531-8286", 
        "trips": [{
            "id": 1,
            "date": 'Wed, 26 Jan 2022 11:25:57 GMT',
            "season": "2021-2022"
        }]
    } in all_players

def test_update_player_username_no_trips(client, two_players_one_trip):
    # Act
    request_body = {
        "username": "rbodart"
    }
    response = client.patch(f'/players/2?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    all_players = client.get(f'/players?API_KEY={API_KEY}').get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "rbodart successfully updated"
    assert {
        "id": 2,
        "username": "rbodart",
        "phone": "+1 (503) 707-9797", 
        "trips": []
    } in all_players

def test_update_player_username_taken(client, two_players_one_trip):
    # Act
    request_body = {
        "username": "reneebodart"
    }
    response = client.patch(f'/players/1?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "username": "Sorry, that username is taken"
    }

def test_update_player_phone_taken(client, two_players_one_trip):
    # Act
    request_body = {
        "phone": "+1 (503) 707-9797"
    }
    response = client.patch(f'/players/1?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "phone": 'The phone number you entered is already registered with an account'
    }

def test_update_player_duplicate(client, two_players_one_trip):
    # Act
    request_body = {
        "phone": "+1 (503) 707-9797",
        "username": "reneebodart"
    }
    response = client.patch(f'/players/1?API_KEY={API_KEY}', json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "phone": 'The phone number you entered is already registered with an account',
        "username": "Sorry, that username is taken"
    }

# POST /trips endpoint

def test_post_trip(client):
    # Act
    response = client.post(f'/players/1?API_KEY={API_KEY}')
    response_body = response.get_json()

    # Assert
    response.status_code == 200
    response_body == "Trip successfully created"

# POST /players_trips endpoint

def test_post_trip_to_player(client, two_players_one_trip):
    # Act
    response = client.post(f'/players_trips?API_KEY={API_KEY}&trip_id=1&player_id=2')
    response_body = response.get_json()

    renees_trips = client.get(f'/players/2?API_KEY={API_KEY}').get_json()["trips"]

    # Assert
    response.status_code == 200
    response_body == "trip successfully added to rbodart's profile"
    assert {
            "id": 1,
            "date": 'Wed, 26 Jan 2022 11:25:57 GMT',
            "season": "2021-2022"
        } in renees_trips

def test_post_nonexistent_trip_to_player(client, two_players_one_trip):
    # Act
    response = client.post(f'/players_trips?API_KEY={API_KEY}&trip_id=2&player_id=2')

    # Assert
    response.status_code == 404

def test_post_trip_to_nonexistent_player(client, two_players_one_trip):
    # Act
    response = client.post(f'/players_trips?API_KEY={API_KEY}&trip_id=1&player_id=55')

    # Assert
    response.status_code == 404