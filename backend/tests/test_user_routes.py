from .environment import TestEnvironment
from app.models import User, Deck, Card
from app.extensions import db
from flask import Flask, jsonify
import unittest
import sys
print(sys.path)


class TestUserRoutes(TestEnvironment):

    def test_create_user(self):
        response = self.client.post(
            '/users', json={'username': 'testuser2', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)

    def test_create_user_no_username(self):
        response = self.client.post(
            '/users', json={'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Username and password are required')

    def test_create_user_no_password(self):
        response = self.client.post('/users', json={'username': 'testuser2'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Username and password are required')

    def test_create_duplicate_user(self):
        response = self.client.post(
            '/users', json={'username': 'John', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Username already exists')

    def test_get_user(self):
        response = self.client.get('/users/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_user(self):
        response = self.client.get('/users/4')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'User not found')

    def test_search_users(self):
        user1 = User(username='test_user1', password='testpassword')
        user2 = User(username='test_user2', password='testpassword')
        user3 = User(username='otheruser', password='testpassword')

        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.commit()

        response = self.client.get('/users')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 6)

        self.assertEqual(data[0]['username'], 'Alfred')
        self.assertEqual(data[1]['username'], 'John')
        self.assertEqual(data[2]['username'], 'Admin')
        self.assertEqual(data[3]['username'], 'test_user1')
        self.assertEqual(data[4]['username'], 'test_user2')
        self.assertEqual(data[5]['username'], 'otheruser')

    def test_search_users_query(self):
        user1 = User(username='test_user1', password='testpassword')
        user2 = User(username='test_user2', password='testpassword')

        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        response = self.client.get('/users?q=test_user')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['username'], 'test_user1')
        self.assertEqual(data[1]['username'], 'test_user2')

    def test_search_users_query_limit(self):
        user1 = User(username='test_user1', password='testpassword')
        user2 = User(username='test_user2', password='testpassword')

        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        response = self.client.get('/users?q=test_user&limit=1')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

        self.assertEqual(data[0]['username'], 'test_user1')

    def test_search_users_query_limit_offset(self):
        user1 = User(username='test_user1', password='testpassword')
        user2 = User(username='test_user2', password='testpassword')

        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        response = self.client.get('/users?q=test_user&limit=1&offset=1')
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

        self.assertEqual(data[0]['username'], 'test_user2')

    def test_update_user(self):
        request_data = {
            'username': 'updateduser',
            'current_password': 'testpassword',
            'password': 'newpassword'
        }
        response = self.client.put(
            '/users/1', json=request_data, headers=self.authorization1)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)

        user = db.session.get(User, 1)
        self.assertEqual(user.username, 'updateduser')

    def test_update_admin_user(self):
        response = self.client.put(
            '/users/1', json={'admin': True}, headers=self.authorization3)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)

        user = db.session.get(User, 1)
        self.assertEqual(user.admin, True)

    def test_update_deleted_request_user(self):
        self.client.delete('/users/3', headers=self.authorization3)
        response = self.client.put(
            '/users/1', json={'username': 'updateduser'}, headers=self.authorization3)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)

    def test_update_unauthorized_request_user(self):
        response = self.client.put(
            '/users/1', json={'username': 'updateduser'}, headers=self.authorization2)
        data = response.get_json()

        self.assertEqual(response.status_code, 403)

    def test_update_admin_unauthorized_request_user(self):
        response = self.client.put(
            '/users/1', json={'admin': True}, headers=self.authorization1)
        data = response.get_json()

        self.assertEqual(response.status_code, 403)

    def test_update_nonexistent_user(self):
        response = self.client.put(
            '/users/4', json={'username': 'updateduser'}, headers=self.authorization1)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)

    def test_update_password_no_current(self):
        request_data = {
            'username': 'updateduser',
            'password': 'newpassword'
        }
        response = self.client.put(
            '/users/1', json=request_data, headers=self.authorization1)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)

    def test_update_password_wrong_current(self):
        request_data = {
            'username': 'updateduser',
            'current_password': 'wrongpassword',
            'password': 'newpassword'
        }
        response = self.client.put(
            '/users/1', json=request_data, headers=self.authorization1)
        data = response.get_json()

        self.assertEqual(response.status_code, 401)

    def test_delete_user(self):
        response = self.client.delete('/users/1', headers=self.authorization1)
        response = self.client.delete('/users/2', headers=self.authorization2)
        data = response.get_json()

        user = db.session.get(User, 1)
        deck = db.session.get(Deck, 1)
        card = db.session.get(Card, 1)

        self.assertIsNone(user)
        self.assertIsNone(deck)
        self.assertIsNone(card)

        self.assertEqual(response.status_code, 200)

    def test_delete_nonxistent_user(self):
        response = self.client.delete('/users/4', headers=self.authorization1)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)

    def test_delete_nonxistent_request_user(self):
        self.client.delete('/users/3', headers=self.authorization3)
        response = self.client.delete('/users/1', headers=self.authorization3)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)

    def test_delete_unauthorized_request_user(self):
        response = self.client.delete('/users/1', headers=self.authorization2)
        data = response.get_json()

        self.assertEqual(response.status_code, 403)

    def test_add_deck(self):
        response = self.client.post(
            '/users/1/decks/3', headers=self.authorization1)
        self.assertEqual(response.status_code, 201)

        deck = db.session.get(Deck, 4)
        self.assertNotEqual(deck, None)

    def test_add_deck_nonxistent_user(self):
        response = self.client.post(
            '/users/4/decks/1', headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

        deck = db.session.get(Deck, 5)
        self.assertIsNone(deck)

    def test_add_deck_nonxistent_request_user(self):
        self.client.delete('/users/3', headers=self.authorization3)
        response = self.client.post(
            '/users/1/decks/1', headers=self.authorization3)
        self.assertEqual(response.status_code, 404)

        deck = db.session.get(Deck, 5)
        self.assertIsNone(deck)

    def test_add_deck_unauthorized_request_user(self):
        response = self.client.post(
            '/users/1/decks/1', headers=self.authorization2)
        self.assertEqual(response.status_code, 403)

        deck = db.session.get(Deck, 5)
        self.assertIsNone(deck)

    def test_add_nonexistent_deck(self):
        response = self.client.post(
            '/users/1/decks/10', headers=self.authorization1)
        self.assertEqual(response.status_code, 404)

        deck = db.session.get(Deck, 5)
        self.assertIsNone(deck)

    def test_search_user_decks(self):
        response = self.client.get(
            '/users/1/decks', headers=self.authorization1)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()['data']
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['name'], 'Javanese')
        self.assertEqual(data[1]['name'], 'Japanese')

    def test_search_user_decks_count_cards(self):
        response = self.client.get(
            '/users/1/decks?card_count=all,new,due', headers=self.authorization1)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()['data']
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['name'], 'Javanese')
        self.assertEqual(data[0]['new_count'], 0)
        self.assertEqual(data[0]['due_count'], 0)
        self.assertEqual(data[0]['all_count'], 0)
        self.assertEqual(data[1]['name'], 'Japanese')
        self.assertEqual(data[1]['new_count'], 0)
        self.assertEqual(data[1]['due_count'], 0)
        self.assertEqual(data[1]['all_count'], 0)

    def test_search_user_decks_query(self):
        response = self.client.get(
            '/users/1/decks?q=Jav', headers=self.authorization1)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    def test_search_user_decks_limit(self):
        response = self.client.get(
            '/users/1/decks?limit=1', headers=self.authorization1)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Javanese')

    def test_search_user_decks_limit_offset(self):
        response = self.client.get(
            '/users/1/decks?limit=1&offset=1', headers=self.authorization1)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Japanese')

    def test_search_nonexistent_user_decks(self):
        response = self.client.get(
            '/users/4/decks', headers=self.authorization1)

        self.assertEqual(response.status_code, 404)

    def test_search_user_decks_nonexistent_request_user(self):
        self.client.delete('/users/3', headers=self.authorization3)
        response = self.client.get(
            '/users/1/decks', headers=self.authorization3)

        self.assertEqual(response.status_code, 404)

    def test_search_user_decks_nonexistent_unauthorized_user(self):
        response = self.client.get(
            '/users/1/decks', headers=self.authorization2)

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
