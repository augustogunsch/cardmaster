import unittest
import json
from app.extensions import db
from app.models import Card
from .environment import TestEnvironment

class TestAuthRoutes(TestEnvironment):

    def test_auth(self):
        login = {'username': 'Alfred', 'password': 'testpassword'}
        response = self.client.post('/auth', json=login)
        self.assertEqual(response.status_code, 200)

    def test_auth_no_user(self):
        login = {'password': 'testpassword'}
        response = self.client.post('/auth', json=login)
        self.assertEqual(response.status_code, 400)

    def test_auth_no_password(self):
        login = {'username': 'Alfred'}
        response = self.client.post('/auth', json=login)
        self.assertEqual(response.status_code, 400)

    def test_auth_user_not_found(self):
        login = {'username': 'Alfred2', 'password': 'testpassword'}
        response = self.client.post('/auth', json=login)
        self.assertEqual(response.status_code, 404)

    def test_auth_invalid_password(self):
        login = {'username': 'Alfred', 'password': 'testpassword123'}
        response = self.client.post('/auth', json=login)
        self.assertEqual(response.status_code, 401)

    def test_auth_invalid_token(self):
        data = {'front': 'Front of Card', 'back': 'Back of Card'}
        authorization = {'Authorization': 'invalid_token'}
        response = self.client.post('/deck/1/card', json=data, headers=authorization)
        self.assertEqual(response.status_code, 401)
        card = db.session.get(Card, 4)
        self.assertIsNone(card)

    def test_auth_no_token(self):
        data = {'front': 'Front of Card', 'back': 'Back of Card'}
        response = self.client.post('/deck/1/card', json=data)
        self.assertEqual(response.status_code, 400)
        card = db.session.get(Card, 4)
        self.assertIsNone(card)

if __name__ == '__main__':
    unittest.main()
