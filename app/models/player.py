from app import db

class Player(db.Model):
    username = db.Column(db.String, primary_key=True)
    phone_number = db.Column(db.String)

    def to_dict(self):
        return {
            "username": self.username,
            "phone": self.phone_number
        }