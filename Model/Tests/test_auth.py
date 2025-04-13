import unittest
from unittest.mock import patch
from Model.app import create_app


class TestAuthenticationController(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()


    @patch('Model.Controllers.auth_controller.get_user_by_username', return_value=(1, "Georgie", "$something$"))
    @patch('Model.Controllers.auth_controller.bcrypt.checkpw', return_value=True)
    def test_login_success(self, mock_get_user, mock_check_password):
        """Teszt helyes jelszóval való bejelentkezésre"""

        payload = {"username": "Georgie", "password": "good_passwordd"}
        response = self.client.post('/auth/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.get_data(as_text=True))


    def test_login_missing_fields(self):
        """Teszt bejelentkezés hiányzó adatokkal"""

        response = self.client.post('/auth/login', json={"username": "Georgie"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username and password required", response.get_data(as_text=True))


    def test_login_invalid_json(self):
        """Teszt bejelentkezés helytelen json fájllal"""

        response = self.client.post('/auth/login', data='not_valid_json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON format", response.get_data(as_text=True))


    @patch('Model.Controllers.auth_controller.get_user_by_username', return_value=(1, "Georgie", "$something$"))
    @patch('Model.Controllers.auth_controller.bcrypt.checkpw', return_value=False)
    def test_wrong_password(self,mock_get_user, mock_check_password):
        """Teszt helytelen jelszóval való bejelentkezésre"""
        payload = {"username": "Georgie", "password": "wrong_password"}
        response = self.client.post('/auth/login', json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.get_data(as_text=True))


    @patch('Model.Controllers.auth_controller.get_user_by_username', return_value=None)
    def test_user_not_in_database(self, mock_check):
        """Teszt bejelentkezés nem létező felhasználóval az adatbázisban"""

        payload = {"username": "Georgie", "password": "something"}
        response = self.client.post('/auth/login', json=payload)
        self.assertEqual(response.status_code, 402)
        self.assertIn("User is not in the database", response.get_data(as_text=True))



if __name__ == '__main__':
    unittest.main()
