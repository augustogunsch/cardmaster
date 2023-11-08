import unittest
import os
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Deck, Card


class TestEnvironment(unittest.TestCase):

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)
        return obj

    def setUp(self):
        os.environ['FLASK_DEBUG'] = '1'
        os.environ['FLASK_TESTING'] = '1'
        os.environ['FLASK_SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        os.environ['FLASK_SECRET_KEY'] = 'wajdlkawjdklawdn293io2njkWDANJKdlkdhawjkhdn%@AD!!@#!@$@'

        self.app = create_app()
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.user1 = self.add(User(
            username='Alfred',
            password='testpassword'
        ))
        self.user2 = self.add(User(
            username='John',
            password='testpassword'
        ))
        self.user3 = self.add(User(
            username='Admin',
            password='testpassword',
            admin=True
        ))

        self.deck1 = self.add(Deck(
            name='Javanese',
            user=self.user1,
            shared=True
        ))
        self.deck2 = self.add(Deck(
            name='Japanese',
            user=self.user1,
            shared=True
        ))
        self.deck3 = self.add(Deck(
            name='German',
            user=self.user2,
            shared=True
        ))
        self.deck4 = self.add(Deck(
            name='Polish',
            user=self.user2,
            shared=False
        ))

        self.card1 = self.add(Card(
            front='apfel',
            back='apple',
            deck=self.deck3
        ))
        self.card2 = self.add(Card(
            front='frau',
            back='woman',
            deck=self.deck3,
            last_revised=datetime.now() - timedelta(days=1),
            revision_due=datetime.now(),
            knowledge_level=1
        ))
        self.card3 = self.add(Card(
            front='frau',
            back='woman',
            deck=self.deck4
        ))

        auth_response = self.client.post('/api/auth', json={
            'username': 'Alfred',
            'password': 'testpassword',
            'tzutcdelta': 0
        })
        self.authorization1 = {'Authorization': auth_response.json['token']}

        auth_response = self.client.post('/api/auth', json={
            'username': 'John',
            'password': 'testpassword',
            'tzutcdelta': 0
        })
        self.authorization2 = {'Authorization': auth_response.json['token']}

        auth_response = self.client.post('/api/auth', json={
            'username': 'Admin',
            'password': 'testpassword',
            'tzutcdelta': 0
        })
        self.authorization3 = {'Authorization': auth_response.json['token']}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()
