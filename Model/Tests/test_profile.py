import unittest
from unittest.mock import patch
from Model.app import create_app


class TestProfileController(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    # /profile/pictures testcases

    @patch('Model.Controllers.profile_controller.get_images_by_user', return_value=[{"image_url": "uploads/some_image.jpg", "predicted_label": "fracture"}])
    def test_get_uploaded_images_success(self, mock_get_images):
        """Teszt képek lekérésére, létező ID-val"""

        response = self.client.get('/profile/pictures?id=222')
        self.assertEqual(response.status_code, 200)
        self.assertIn("image_url", response.get_data(as_text=True))
        self.assertIn("fracture", response.get_data(as_text=True))


    def test_get_uploaded_images_missing_id(self):
        """Teszt, ahol az ID hiányzik"""
        response = self.client.get('/profile/pictures')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.get_data(as_text=True))


    @patch('Model.Controllers.profile_controller.get_images_by_user', return_value=None)
    def test_get_uploaded_images_no_images(self, mock_get_images):
        """Teszt képek lekérésére nem létező ID-val"""

        response = self.client.get('/profile/pictures?id=222')
        self.assertEqual(response.status_code, 401)
        self.assertIn("No uploaded images found for this user", response.get_data(as_text=True))

    # /profile/personal_data testcases

    @patch('Model.Controllers.profile_controller.get_user_by_username', return_value=(1, "Georgie", "$hashedpassword$", "georgie@something.com", 22))
    def test_get_personal_data_success(self, mock_get_user):
        """Teszt, ahol létező felhasználónévhez visszakapjuk a helyes adatokat"""

        response = self.client.get('/profile/personal_data?username=Georgie')
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.get_data(as_text=True))
        self.assertIn("email", response.get_data(as_text=True))
        self.assertIn("age", response.get_data(as_text=True))


    def test_get_personal_data_missing_username(self):
        """Teszt, ahol a felhasználónév hiányzik"""

        response = self.client.get('/profile/personal_data')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username is required", response.get_data(as_text=True))


    @patch('Model.Controllers.profile_controller.get_user_by_username', return_value=None)
    def test_get_personal_data_no_user(self, mock_get_user):
        """Teszt, ahol nem létező felhasználónevet használunk"""
        response = self.client.get('/profile/personal_data?username=not_real_username')
        self.assertEqual(response.status_code, 401)
        self.assertIn("No user found with the given name", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()