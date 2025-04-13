import sqlite3
from Model import config
import os
from datetime import datetime

#THINK ABOUT LOGGING IF EXCEPTION OCCURS

UPLOAD_FOLDER = config.UPLOADS_PATH
TEST_UPLOAD_FOLDER = config.TEST_UPLOADS_PATH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEST_UPLOAD_FOLDER, exist_ok=True)

def get_db_connection(db_type):
    """Létrehozza és visszaadja az adatbázis kapcsolatot."""
    if db_type == "prod":
        conn = sqlite3.connect(config.DB_PATH)
    else:
        conn = sqlite3.connect(config.TEST_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database(db_type):
    """Inicializálja az adatbázist és létrehozza a szükséges táblákat."""
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        with get_db_connection(db_type) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL
            )''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                predicted_label TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')

            conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")

def insert_user(username, email, password, age, db_type):
    """Beszúr egy új felhasználót az adatbázisba, majd visszadja, hogy a művelet sikeres volt-e."""
    try:
        with get_db_connection(db_type) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password, age) VALUES (?, ?, ?, ?)",
                (username, email, password, age),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("Error: Username already exists.")
        else:
            print(f"Integrity Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False


def get_user_by_username(username, db_type):
    """Visszaadja egy felhasználó adatait felhasználónév és jelszó alapján"""
    try:
        with get_db_connection(db_type) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            data = cursor.fetchone()
            if not data:
                return None
            return data
    except Exception as e:
        print(f"Error getting the data by username: {username}. {e}")
        return None


def insert_image(user_id, uploaded_file, predicted_label, db_type):
    """Adott képet eltárol egy specifikus mappába, majd eltárolja a felhasználó ID-ját,
    a kép elérési útját és becsült címkéjét az adatbázisban."""
    try:
        timestamp = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        filename = f"user_{user_id}_{timestamp}"
        if db_type == "prod":
            file_path = os.path.join(UPLOAD_FOLDER, filename)
        else:
            file_path = os.path.join(TEST_UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with get_db_connection(db_type) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO images (user_id, image_path, predicted_label) VALUES (?, ?, ?)",
                           (user_id, file_path, predicted_label))
            conn.commit()
        return file_path
    except Exception as e:
        print(f"Error saving image or inserting into database: {e}")
        return None


def get_images_by_user(user_id, db_type):
    """Visszaadja egy adott felhasználó által feltöltött összes képet és hozzátartozó becsült címkéket."""
    try:
        with get_db_connection(db_type) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT image_path, predicted_label FROM images WHERE user_id = ?", (user_id,))
            images = cursor.fetchall()

            if not images:
                return []

            return [{"image_url": os.path.join(UPLOAD_FOLDER, image[0]), "predicted_label": image[1]} for image in images]

    except Exception as e:
        print(f"Error fetching images for user {user_id}: {e}")
        return []


def drop_tables(db_type):
    """Drops all tables in the database."""
    try:
        with get_db_connection(db_type) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("DROP TABLE IF EXISTS images")
            conn.commit()
            print("Tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")