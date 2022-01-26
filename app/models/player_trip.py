from app import db

class PlayerTrip(db.Model):
    __tablename__ = "players_trips"
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), primary_key=True, nullable=False)
    username = db.Column(db.String, db.ForeignKey("players.username"), primary_key=True, nullable=False)