import unittest
from app import create_app
from app.extensions import db
from app.models import User, Deck, Card
from .config import Config

class TestEnvironment(unittest.TestCase):

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)
        return obj

    def setUp(self):
        self.app = create_app(Config)
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.user1 = self.add(User(username='Alfred', password='testpassword'))
        self.user2 = self.add(User(username='John', password='testpassword'))

        self.deck1 = self.add(Deck(name='Javanese', user=self.user1, author=self.user1, shared=True))
        self.deck2 = self.add(Deck(name='Japanese', user=self.user1, author=self.user1, shared=True))
        self.deck3 = self.add(Deck(name='German', user=self.user2, author=self.user2, shared=True))
        self.deck4 = self.add(Deck(name='Polish', user=self.user2, author=self.user2, shared=False))

        self.card1 = self.add(Card(front='apfel', back='apple', deck=self.deck3))
        self.card2 = self.add(Card(front='frau', back='woman', deck=self.deck3))
        self.card3 = self.add(Card(front='frau', back='woman', deck=self.deck4))

        auth_response = self.client.post('/auth', json={'username': 'Alfred', 'password': 'testpassword'})
        self.authorization1 = {'Authorization': auth_response.json['token']}

        auth_response = self.client.post('/auth', json={'username': 'John', 'password': 'testpassword'})
        self.authorization2 = {'Authorization': auth_response.json['token']}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()
