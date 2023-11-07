from datetime import date, datetime, timedelta
from .card import Card
from ..extensions import db

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shared = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_deck_user_id'), nullable=False)
    user = db.relationship('User', back_populates='decks', foreign_keys=[user_id])
    cards = db.relationship('Card', back_populates='deck', foreign_keys=[Card.deck_id], cascade='all, delete-orphan')

    def get_json(self, cards_count=None, tzutcdelta=None):
        value = {
            'id': self.id,
            'name': self.name,
            'user': self.user.username,
            'shared': self.shared,
        }

        if cards_count:
            if 'due' in cards_count:
                now = datetime.utcnow()

                if tzutcdelta == None:
                    delta = timedelta(seconds=self.user.tzutcdelta)
                else:
                    delta = timedelta(seconds=tzutcdelta)

                query = Card.query.filter(Card.deck_id == self.id) \
                                  .filter(Card.revision_due <= now + delta)
                value['due_count'] = query.count()

            if 'all' in cards_count:
                query = Card.query.filter(Card.deck_id == self.id)
                value['all_count'] = query.count()

            if 'new' in cards_count:
                query = Card.query.filter(Card.deck_id == self.id) \
                                  .filter(Card.knowledge_level == 0)
                value['new_count'] = query.count()

        return value
