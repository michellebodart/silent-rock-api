from app import db

class PlayerTrip(db.Model):
    __tablename__ = "players_trips"
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), primary_key=True, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), primary_key=True, nullable=False)