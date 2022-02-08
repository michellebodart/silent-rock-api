from app import db

class PendingPlayerTrip(db.Model):
    __tablename__ = "pending_players_trips"
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), primary_key=True, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), primary_key=True, nullable=False)
    trip_owner_id = db.Column(db.Integer)