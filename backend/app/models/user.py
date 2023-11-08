from ..extensions import db
from .deck import Deck
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(162), nullable=False)
    decks = db.relationship('Deck', back_populates='user', foreign_keys=[
                            Deck.user_id], cascade='all, delete-orphan')
    admin = db.Column(db.Boolean, default=False)
    # used internally for calculating dates
    tzutcdelta = db.Column(db.Integer, default=0)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.set_password(password)
        self.admin = admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'admin': self.admin
        }
