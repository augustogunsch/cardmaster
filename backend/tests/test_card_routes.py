import unittest
import json
from flask import Flask
from app import create_app
from app.extensions import db
from app.models import User, Deck, Card
from .config import Config

class TestCardRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app(Config)
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.user = User(username='testuser', password='testpassword')
        db.session.add(self.user)
        db.session.commit()
        db.session.refresh(self.user)
        self.deck = Deck(name='Test Deck', owner=self.user)
        db.session.add(self.deck)
        db.session.commit()
        db.session.refresh(self.deck)

        auth_response = self.client.post('/auth', json={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(auth_response.status_code, 200)
        self.authorization = {'Authorization': auth_response.json['token']}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_create_card(self):
        data = {'front': 'Front of Card', 'back': 'Back of Card'}
        response = self.client.post(f'/decks/{self.deck.id}/cards', json=data, headers=self.authorization)
        self.assertEqual(response.status_code, 201)

    def test_get_cards(self):
        response = self.client.get(f'/decks/{self.deck.id}/cards', headers=self.authorization)
        self.assertEqual(response.status_code, 200)
        card_list = response.json
        self.assertEqual(len(card_list), 0)  # Assuming no cards were created yet

    def test_get_card(self):
        card = Card(front='Front of Card', back='Back of Card', deck=self.deck)
        db.session.add(card)
        db.session.commit()
        response = self.client.get(f'/cards/{card.id}', headers=self.authorization)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['data']['front'], 'Front of Card')

    def test_update_card(self):
        card = Card(front='Front of Card', back='Back of Card', deck=self.deck)
        db.session.add(card)
        db.session.commit()
        data = {'front': 'Updated Front', 'back': 'Updated Back'}
        response = self.client.put(f'/cards/{card.id}', json=data, headers=self.authorization)
        self.assertEqual(response.status_code, 200)
        updated_card = db.session.get(Card, card.id)
        self.assertEqual(updated_card.front, 'Updated Front')

    def test_delete_card(self):
        card = Card(front='Front of Card', back='Back of Card', deck=self.deck)
        db.session.add(card)
        db.session.commit()
        response = self.client.delete(f'/cards/{card.id}', headers=self.authorization)
        self.assertEqual(response.status_code, 200)
        deleted_card = db.session.get(Card, card.id)
        self.assertIsNone(deleted_card)

if __name__ == '__main__':
    unittest.main()
