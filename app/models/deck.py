from ..extensions import db
from .card import Card

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shared = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_deck_user_id'), nullable=False)
    user = db.relationship('User', back_populates='decks', foreign_keys=[user_id])
    cards = db.relationship('Card', back_populates='deck', foreign_keys=[Card.deck_id], cascade='all, delete-orphan')

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user': self.user.username,
            'shared': self.shared,
            'cards_count': len(self.cards)
        }
