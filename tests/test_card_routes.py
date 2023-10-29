import unittest
import json
from flask import Flask
from app.extensions import db
from app.models import Card, Deck
from .environment import TestEnvironment

class TestCardRoutes(TestEnvironment):

    def test_create_card(self):
        data = {'front': 'Front of Card', 'back': 'Back of Card'}
        response = self.client.post('/decks/1/cards', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 201)
        card1 = db.session.get(Card, 4)
        self.assertIsNotNone(card1)
        card2 = db.session.get(Card, 5)
        self.assertIsNone(card2)

    def test_create_card_user_deleted(self):
        self.client.delete('/users/1', headers=self.authorization1)
        data = {'front': 'Front of Card', 'back': 'Back of Card'}
        response = self.client.post('/decks/1/cards', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 404)
        card = db.session.get(Card, 4)
        self.assertIsNone(card)

    def test_create_card_deck_deleted(self):
        self.client.delete('/decks/1', headers=self.authorization1)
        data = {'front': 'Front of Card', 'back': 'Back of Card'}
        response = self.client.post('/decks/1/cards', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 404)
        card = db.session.get(Card, 4)
        self.assertIsNone(card)

    def test_create_card_others_deck(self):
        data = {'front': 'Front of Card', 'back': 'Back of Card'}
        response = self.client.post('/decks/3/cards', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 403)
        card = db.session.get(Card, 4)
        self.assertIsNone(card)

    def test_create_card_no_front(self):
        data = {'back': 'Back of Card'}
        response = self.client.post('/decks/1/cards', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 400)
        card = db.session.get(Card, 4)
        self.assertIsNone(card)

    def test_create_card_no_back(self):
        data = {'front': 'Front of Card'}
        response = self.client.post('/decks/1/cards', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 400)
        card = db.session.get(Card, 4)
        self.assertIsNone(card)

    def test_create_card_reverse(self):
        data = {'front': 'Front of Card', 'back': 'Back of Card', 'reverse': True}
        response = self.client.post('/decks/1/cards', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 201)
        card1 = db.session.get(Card, 4)
        self.assertIsNotNone(card1)
        self.assertEqual(card1.front, 'Front of Card')
        self.assertEqual(card1.back, 'Back of Card')
        card2 = db.session.get(Card, 5)
        self.assertIsNotNone(card2)
        self.assertEqual(card2.front, 'Back of Card')
        self.assertEqual(card2.back, 'Front of Card')

    def test_search_cards(self):
        response = self.client.get('/decks/3/cards', headers=self.authorization2)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['front'], 'apfel')
        self.assertEqual(data[1]['front'], 'frau')

    def test_search_cards_user_deleted(self):
        self.client.delete('/users/2', headers=self.authorization2)
        response = self.client.get('/decks/3/cards', headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_search_cards_nonexistent_deck(self):
        response = self.client.get('/decks/5/cards', headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_search_cards_shared_deck(self):
        response = self.client.get('/decks/3/cards', headers=self.authorization1)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_search_cards_locked_deck(self):
        response = self.client.get('/decks/4/cards', headers=self.authorization1)
        self.assertEqual(response.status_code, 403)

    def test_search_cards_query(self):
        response = self.client.get('/decks/3/cards?q=frau', headers=self.authorization2)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['front'], 'frau')

    def test_search_cards_limit(self):
        response = self.client.get('/decks/3/cards?limit=1', headers=self.authorization2)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['front'], 'apfel')

    def test_search_cards_limit_offset(self):
        response = self.client.get('/decks/3/cards?limit=1&offset=1', headers=self.authorization2)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['front'], 'frau')

    def test_get_card(self):
        response = self.client.get('/cards/1', headers=self.authorization2)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()['data']
        self.assertEqual(data['front'], 'apfel')

    def test_get_card_user_deleted(self):
        self.client.delete('/users/2', headers=self.authorization2)
        response = self.client.get('/cards/1', headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_get_nonexistent_card(self):
        response = self.client.get('/cards/5', headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_get_shared_card(self):
        response = self.client.get('/cards/2', headers=self.authorization1)
        self.assertEqual(response.status_code, 200)

    def test_get_locked_card(self):
        response = self.client.get('/cards/3', headers=self.authorization1)
        self.assertEqual(response.status_code, 403)

    def test_update_card(self):
        data = {'front': 'Updated Front', 'back': 'Updated Back'}
        response = self.client.put(f'/cards/1', json=data, headers=self.authorization2)
        self.assertEqual(response.status_code, 200)
        card = db.session.get(Card, 1)
        self.assertEqual(card.front, 'Updated Front')
        self.assertEqual(card.back, 'Updated Back')

    def test_update_card_user_deleted(self):
        self.client.delete('/users/2', headers=self.authorization2)
        data = {'front': 'Updated Front', 'back': 'Updated Back'}
        response = self.client.put(f'/cards/1', json=data, headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_update_nonexistent_card(self):
        data = {'front': 'Updated Front', 'back': 'Updated Back'}
        response = self.client.put(f'/cards/5', json=data, headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_update_others_card(self):
        data = {'front': 'Updated Front', 'back': 'Updated Back'}
        response = self.client.put(f'/cards/1', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 403)

    def test_delete_card(self):
        response = self.client.delete(f'/cards/1', headers=self.authorization2)
        self.assertEqual(response.status_code, 200)
        card = db.session.get(Card, 1)
        self.assertIsNone(card)

    def test_delete_card_user_deleted(self):
        self.client.delete('/users/2', headers=self.authorization2)
        response = self.client.delete(f'/cards/1', headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_card(self):
        response = self.client.delete(f'/cards/5', headers=self.authorization2)
        self.assertEqual(response.status_code, 404)

    def test_delete_others_card(self):
        response = self.client.delete(f'/cards/1', headers=self.authorization1)
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
