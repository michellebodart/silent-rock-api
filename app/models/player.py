from app import db

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    phone_number = db.Column(db.String)
    trips = db.relationship("Trip", secondary="players_trips", backref="players")

    def to_dict(self):
        trips = [trip.to_dict() for trip in self.trips]

        return {
            "id": self.id,
            "username": self.username,
            "phone": self.phone_number,
            "trips": trips
        }