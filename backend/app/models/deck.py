from ..extensions import db
from .card import Card

deck_user_association = db.Table(
    'deck_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('deck_id', db.Integer, db.ForeignKey('deck.id'))
)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shared = db.Column(db.Boolean, default=False)
    users = db.relationship('User', secondary=deck_user_association, back_populates='decks')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_deck_owner_id'), nullable=False)
    owner = db.relationship('User', back_populates='decks_owned', foreign_keys=[owner_id])
    cards = db.relationship('Card', back_populates='deck', foreign_keys=[Card.deck_id])

    def __repr__(self):
        return f'<Deck {self.name}>'
