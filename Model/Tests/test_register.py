import unittest
from unittest.mock import patch
from Model.app import create_app


class TestRegisterController(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('Model.Controllers.register_controller.insert_user', return_value=True)
    def test_register_success(self, mock_insert_user):
        """Teszt sikeres regisztrációra"""
        payload = {
            "username": "georgie",
            "email": "georgie@something.com",
            "password": "something",
            "age": 30
        }
        response = self.client.post('/register/register', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("User registered successfully", response.get_data(as_text=True))

    def test_register_missing_fields(self):
        """Teszt regisztráció hiányzó adatokkal"""
        payload = {
            "username": "georgie",
            "email": "georgie@something.com",
            # missing password
            "age": 30
        }
        response = self.client.post('/register/register', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.get_data(as_text=True))

    @patch('Model.Controllers.register_controller.insert_user', return_value=False)
    def test_register_user_exists(self, mock_insert_user):
        """Teszt regisztráció már létező email címmel vagy felhasználónévvel"""
        payload = {
            "username": "georgie",
            "email": "georgie@something.com",
            "password": "something",
            "age": 30
        }
        response = self.client.post('/register/register', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Username or email already exists", response.get_data(as_text=True))





if __name__ == '__main__':
    unittest.main()
