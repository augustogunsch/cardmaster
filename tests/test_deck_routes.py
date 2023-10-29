import unittest
import json
from flask import Flask
from app.extensions import db
from app.models import Deck
from .environment import TestEnvironment

class TestDeckRoutes(TestEnvironment):

    def test_create_deck(self):
        data = {'name': 'New Deck'}
        response = self.client.post('/decks', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 201)

    def test_create_deck_user_deleted(self):
        self.client.delete('/users/1', headers=self.authorization1)
        data = {'name': 'New Deck'}
        response = self.client.post('/decks', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

    def test_create_deck_no_name(self):
        response = self.client.post('/decks', json={}, headers=self.authorization1)
        self.assertEqual(response.status_code, 400)

    def test_get_deck(self):
        response = self.client.get(f'/decks/1', headers=self.authorization1)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['name'], 'Javanese')

    def test_get_deck_user_deleted(self):
        self.client.delete('/users/1', headers=self.authorization1)
        response = self.client.get(f'/decks/1', headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

    def test_get_nonexistent_deck(self):
        response = self.client.get(f'/decks/5', headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

    def test_get_others_deck(self):
        response = self.client.get(f'/decks/4', headers=self.authorization1)
        self.assertEqual(response.status_code, 403)

    def test_update_deck(self):
        data = {'name': 'Updated Deck', 'shared': False}
        response = self.client.put(f'/decks/1', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 200)
        updated_deck = db.session.get(Deck, 1)
        self.assertEqual(updated_deck.name, 'Updated Deck')
        self.assertEqual(updated_deck.shared, False)

    def test_update_deck_user_deleted(self):
        self.client.delete('/users/1', headers=self.authorization1)
        data = {'name': 'Updated Deck'}
        response = self.client.put(f'/decks/1', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

    def test_update_nonexistent_deck(self):
        data = {'name': 'Updated Deck'}
        response = self.client.put(f'/decks/5', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

    def test_update_others_deck(self):
        data = {'name': 'Updated Deck'}
        response = self.client.put(f'/decks/3', json=data, headers=self.authorization1)
        self.assertEqual(response.status_code, 403)

    def test_delete_deck(self):
        response = self.client.delete(f'/decks/1', headers=self.authorization1)
        self.assertEqual(response.status_code, 200)
        deleted_deck = db.session.get(Deck, 1)
        self.assertIsNone(deleted_deck)

    def test_delete_deck_user_deleted(self):
        self.client.delete('/users/1', headers=self.authorization1)
        response = self.client.delete(f'/decks/1', headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_deck(self):
        response = self.client.delete(f'/decks/5', headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

    def test_delete_others_deck(self):
        response = self.client.delete(f'/decks/3', headers=self.authorization1)
        self.assertEqual(response.status_code, 403)

    def test_search_decks(self):
        response = self.client.get('/decks')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)

        self.assertEqual(data[0]['name'], 'Javanese')
        self.assertEqual(data[1]['name'], 'Japanese')
        self.assertEqual(data[2]['name'], 'German')

    def test_search_decks_count(self):
        response = self.client.get('/decks?count=true')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, 3)

    def test_search_decks_query(self):
        response = self.client.get('/decks?q=nese')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['name'], 'Javanese')
        self.assertEqual(data[1]['name'], 'Japanese')

    def test_search_decks_search_limit(self):
        response = self.client.get('/decks?q=nese&limit=1')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

        self.assertEqual(data[0]['name'], 'Javanese')

    def test_search_decks_limit_offset(self):
        response = self.client.get('/decks?q=nese&limit=1&offset=1')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

        self.assertEqual(data[0]['name'], 'Japanese')

if __name__ == '__main__':
    unittest.main()
