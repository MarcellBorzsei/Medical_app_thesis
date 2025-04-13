import unittest
import os
from io import BytesIO
from Model.Database import conn
from Model import config

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        conn.drop_tables("test")
        conn.initialize_database("test")

    def tearDown(self):
        conn.drop_tables("test")

    def test_insert_and_fetch_user(self):
        """Teszt felhasználó beszúrására és lekérdezésére"""

        result = conn.insert_user("Georgie", "georgie@something.com", "something", 22, "test")
        self.assertTrue(result)

        user = conn.get_user_by_username("Georgie", "test")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "Georgie")
        self.assertEqual(user["email"], "georgie@something.com")


    def test_unique_constraint_fail(self):
        """Teszt az egyedi megszorítás megsértésére"""
        conn.insert_user("Georgie", "georgie@something.com", "something", 22, "test")
        result = conn.insert_user("Georgie", "georgie@something.com", "something", 22, "test")
        self.assertFalse(result)


    def test_get_not_existing_user(self):
        """Teszt nem létező felhasználó lekérésére"""
        user = conn.get_user_by_username("Not_Georgie", "test")
        self.assertIsNone(user)


    def test_insert_image_and_fetch(self):
        """Teszt kép beszúrására és lekérdezésére"""
        os.makedirs(config.TEST_UPLOADS_PATH, exist_ok=True)

        conn.insert_user("Georgie", "georgie@something.com", "something", 22, "test")
        user = conn.get_user_by_username("Georgie", "test")

        test_image = BytesIO(b"some_image_content")
        test_image.name = "test.jpg"
        file_path = conn.insert_image(user["id"], test_image, "fractured", "test")

        self.assertTrue(os.path.exists(file_path))
        images = conn.get_images_by_user(user["id"], "test")
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["predicted_label"], "fractured")

        os.remove(file_path)


    def test_get_images_when_none(self):
        """Teszt, Képek lekérdezésére, ha a felhasználónak még nincsenek képei"""
        conn.insert_user("Georgie", "georgie@something.com", "something", 22, "test")
        user = conn.get_user_by_username("Georgie", "test")
        images = conn.get_images_by_user(user["id"], "test")
        self.assertEqual(images, [])


if __name__ == '__main__':
    unittest.main()