import unittest
from unittest.mock import patch
from Model.app import create_app
from io import BytesIO

class TestConvertController(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()


    @patch('Model.Controllers.convert_controller.save_uploaded_file', return_value='/something/temp/file.dcm')
    @patch('Model.Controllers.convert_controller.convert_dicom_to_jpg', return_value='/something/temp/file.jpg')
    def test_convert_success(self, mock_convert, mock_save):
        """Teszt sikeres konvertálásra"""
        good_dcm = BytesIO(b'good_DICOM_content')
        data = {'file': (good_dcm, 'good.dcm')}

        response = self.client.post('/convert/convert', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("jpg_file_path", response.get_json())


    def test_convert_missing_file(self):
        """Teszt hiányzó fájl résszel"""
        response = self.client.post('/convert/convert', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file part', response.get_data(as_text=True))


    @patch('Model.Controllers.convert_controller.save_uploaded_file', side_effect=Exception("Saving failed"))
    def test_convert_file_saving_error(self, mock_save):
        """Teszt, ahol a fájl mentése közben hiba történik"""
        wrong_dcm = BytesIO(b'wrong_DICOM_content')
        data = {'file': (wrong_dcm, 'wrong.dcm')}

        response = self.client.post('/convert/convert',data=data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("An error occurred during converting", response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()