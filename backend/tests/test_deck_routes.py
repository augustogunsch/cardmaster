import unittest
import json
from flask import Flask
from app import create_app
from app.extensions import db
from app.models import User, Deck
from .config import Config

class TestDeckRoutes(unittest.TestCase):

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

    def test_create_deck(self):
        data = {'name': 'New Deck'}
        response = self.client.post('/decks', json=data, headers=self.authorization)
        self.assertEqual(response.status_code, 201)

    def test_get_deck(self):
        response = self.client.get(f'/decks/{self.deck.id}', headers=self.authorization)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['name'], 'Test Deck')

    def test_update_deck(self):
        data = {'name': 'Updated Deck'}
        response = self.client.put(f'/decks/{self.deck.id}', json=data, headers=self.authorization)
        self.assertEqual(response.status_code, 200)
        updated_deck = db.session.get(Deck, self.deck.id)
        self.assertEqual(updated_deck.name, 'Updated Deck')

    def test_delete_deck(self):
        response = self.client.delete(f'/decks/{self.deck.id}', headers=self.authorization)
        self.assertEqual(response.status_code, 200)
        deleted_deck = db.session.get(Deck, self.deck.id)
        self.assertIsNone(deleted_deck)

    def test_get_shared_decks(self):
        response = self.client.get('/decks/shared')
        self.assertEqual(response.status_code, 200)

    def test_get_owned_decks(self):
        response = self.client.get('/decks/owned', headers=self.authorization)
        self.assertEqual(response.status_code, 200)

    def test_get_collected_decks(self):
        response = self.client.get('/decks', headers=self.authorization)
        self.assertEqual(response.status_code, 200)

    def test_add_deck_to_collection(self):
        response = self.client.post(f'/decks/add/{self.deck.id}', headers=self.authorization)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
