from app import db

class Player(db.Model):
    __tablename__ = "players"
    username = db.Column(db.String, primary_key=True)
    phone_number = db.Column(db.String)
    trips = db.relationship("Trip", secondary="players_trips", backref="players")

    def to_dict(self):
        trips = [trip.to_dict() for trip in self.trips]

        return {
            "username": self.username,
            "phone": self.phone_number,
            "trips": trips
        }