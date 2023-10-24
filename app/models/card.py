from ..extensions import db
from sqlalchemy import event

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id', name='fk_card_deck_id'), nullable=False)
    deck = db.relationship('Deck', back_populates='cards', foreign_keys=[deck_id])
    revision_due = db.Column(db.Date)
    knowledge_level = db.Column(db.Integer)

    def get_json(self):
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back
        }
