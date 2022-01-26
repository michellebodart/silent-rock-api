from app import db

class Trip(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)

    def to_dict(self):
        if self.date.month < 11:
            season = str(self.date.year-1) + "-" + str(self.date.year)
        else:
            season = str(self.date.year) + "-" + str(self.date.year + 1)

        return {
            "id": self.id,
            "date": self.date,
            "season": season
        }