import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Database", "medical_app.db")
TEST_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Database", "test_medical_app.db")
UPLOADS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Database", "Uploads")
TEST_UPLOADS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Database", "Test_Uploads")
TUMOR_MODEL_PATH = os.path.join(BASE_PATH, "Neural_Networks/Networks/tumor2.h5")
FRACTURE_MODEL_PATH = os.path.join(BASE_PATH, "Neural_Networks/Networks/fracture.h5")
HOST_NUM = "0.0.0.0"
PORT_NUM = 5000
print(TUMOR_MODEL_PATH)