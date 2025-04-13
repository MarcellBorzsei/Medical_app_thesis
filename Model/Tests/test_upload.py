import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from Model.app import create_app


class TestUploadController(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('Model.Controllers.upload_controller.insert_image', return_value='/something/image/test.jpg')
    @patch('Model.Controllers.upload_controller.predict_tumor', return_value=[[0.1, 0.2, 0.0, 0.0, 0.7]])
    @patch('Model.Controllers.upload_controller.preprocess_image', return_value="fake_preprocessed_image")
    def test_tumor_good_prediction(self, mock_preprocess, mock_predict, mock_insert):
        """Teszt a tumor model helyes predikciójához"""

        file = BytesIO(b"good_tumor_image_content")
        data = {
            "file": (file, "test.jpg"),
            "id": "222"
        }

        response = self.client.post('/upload/upload_tumor', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['prediction'],"pituitary")


    @patch('Model.Controllers.upload_controller.insert_image', return_value='/something/image/test.jpg')
    @patch('Model.Controllers.upload_controller.predict_fracture', return_value=[[0.9, 0.05, 0.05]])
    @patch('Model.Controllers.upload_controller.preprocess_image', return_value="fake_preprocessed_image")
    def test_fracture_success(self, mock_preprocess, mock_predict, mock_insert):
        """Teszt a fracture model helyes predikciójához"""

        file = BytesIO(b"good_fracture_image_content")
        data = {
            "file": (file, "fracture.jpg"),
            "id": "222"
        }

        response = self.client.post('/upload/upload_fracture', data=data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.get_json()['prediction'], "fractured")


    def test_missing_file(self):
        """Teszt hianyzó fájl esetén"""
        response = self.client.post('/upload/upload_tumor', data={"id": "222"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file part", response.get_data(as_text=True))

    def test_missing_id(self):
        file = BytesIO(b"something")
        response = self.client.post('/upload/upload_tumor', data={"file": (file, "test.jpg")})
        self.assertEqual(response.status_code, 401)
        self.assertIn("No id part", response.get_data(as_text=True))

    def test_empty_filename(self):
        file = BytesIO(b"something")
        response = self.client.post('/upload/upload_tumor', data={"file": (file, ""), "id": "222"})
        self.assertEqual(response.status_code, 402)
        self.assertIn("No selected file", response.get_data(as_text=True))


    @patch('Model.Controllers.upload_controller.preprocess_image', return_value=None)
    def test_invalid_image(self, mock_preprocess):
        file = BytesIO(b"something")
        data = {
            "file": (file, "test.jpg"),
            "id": "222"
        }
        response = self.client.post('/upload/upload_tumor', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Error processing the image", response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
