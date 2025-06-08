from app import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    tickets_type = db.Column(db.String(50), nullable=False)
