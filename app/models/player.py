from app import db
from app.models.pending_player_trip import PendingPlayerTrip

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    phone_number = db.Column(db.String)
    visible_on_leaderboard = db.Column(db.Boolean)
    trips = db.relationship("Trip", secondary="players_trips", backref="players")
    pending_trips = db.relationship("Trip", secondary="pending_players_trips", backref="players2")

    def to_dict(self):
        trips = [trip.to_dict() for trip in self.trips]
        trips.reverse()

        # pending_trips = [pending_trip.to_dict() for pending_trip in self.pending_trips]

        pending_trips = []
        for pending_trip in self.pending_trips:
            response = pending_trip.to_dict()
            pending_trip_from_join_table = PendingPlayerTrip.query.filter(PendingPlayerTrip.player_id == self.id, PendingPlayerTrip.trip_id == pending_trip.id).first()
            trip_owner_username = pending_trip_from_join_table.trip_owner_username
            response["trip_owner_username"] = trip_owner_username
            pending_trips.append(response)


        pending_trips.reverse()

        return {
            "id": self.id,
            "username": self.username,
            "phone": self.phone_number,
            "trips": trips,
            "pending_trips": pending_trips,
            "visible_on_leaderboard": self.visible_on_leaderboard
        }