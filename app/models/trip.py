from app import db

class Trip(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date
        }