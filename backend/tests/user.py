import unittest
from flask import Flask, jsonify
from app import create_app
from app.extensions import db
from app.models import User
from .config import Config

class UserRoutesTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(Config)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.user = User(username='testuser', password='testpassword')
            db.session.add(self.user)
            db.session.commit()
            db.session.refresh(self.user)

        auth_response = self.client.post('/auth', json={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(auth_response.status_code, 200)
        self.authorization = {'Authorization': auth_response.json['token']}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        response = self.client.post('/users', json={'username': 'testuser2', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User created successfully')

    def test_create_duplicate_user(self):
        response = self.client.post('/users', json={'username': 'testuser', 'password': 'testpassword'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Username already exists')

    def test_get_user(self):
        response = self.client.get('/users/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['username'], 'testuser')

    def test_get_nonexistent_user(self):
        response = self.client.get('/users/2')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'User not found')

    def test_update_user(self):
        response = self.client.put('/user', json={'username': 'updateduser'}, headers=self.authorization)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'User updated successfully')

        with self.app.app_context():
            user = db.session.get(User, 1)
            self.assertEqual(user.username, 'updateduser')

    def test_delete_user(self):
        response = self.client.delete('/user', headers=self.authorization)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'User deleted successfully')

    def test_search_users(self):
        user1 = User(username='test_user1', password='testpassword')
        user2 = User(username='test_user2', password='testpassword')
        user3 = User(username='otheruser', password='testpassword')

        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.commit()

        response = self.client.get('/users/search?q=test_user')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)  # Two users matching the query

        # Ensure the correct users are returned
        self.assertEqual(data[0]['username'], 'test_user1')
        self.assertEqual(data[1]['username'], 'test_user2')

    def test_search_users_no_query(self):
        response = self.client.get('/users/search')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Please provide a search query')

    def test_search_users_not_found(self):
        response = self.client.get('/users/search?q=nonexistent')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'No users found for the given query')

if __name__ == '__main__':
    unittest.main()
