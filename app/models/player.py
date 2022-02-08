from app import db

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

        pending_trips = [pending_trip.to_dict() for pending_trip in self.pending_trips]
        pending_trips.reverse()

        return {
            "id": self.id,
            "username": self.username,
            "phone": self.phone_number,
            "trips": trips,
            "pending_trips": pending_trips,
            "visible_on_leaderboard": self.visible_on_leaderboard
        }