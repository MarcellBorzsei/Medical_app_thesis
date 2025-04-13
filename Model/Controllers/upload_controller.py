from flask import Blueprint, request, jsonify
import numpy as np
from PIL import Image
import io
from keras.api.models import load_model
from keras.api.preprocessing.image import img_to_array
from Model.Database.conn import insert_image
from Model.config import TUMOR_MODEL_PATH, FRACTURE_MODEL_PATH

tumor_model_path = TUMOR_MODEL_PATH
fracture_model_path = FRACTURE_MODEL_PATH

TUMOR_CLASS_LABELS = {0: 'glioma', 1: 'meningioma', 2: 'no_tumor', 3: 'other_tumor', 4: 'pituitary'}
FRACTURE_CLASS_LABELS = {0: 'fractured', 1: 'not_fractured', 2: 'other_fracture'}


upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload_tumor', methods=['POST'])
def prediction_tumor():
    return classify("tumor")

@upload_bp.route('/upload_fracture', methods=['POST'])
def prediction_fracture():
    return classify("fracture")

tumor_model = load_model(tumor_model_path)
fracture_model = load_model(fracture_model_path)

def predict_tumor(image):
    """Tumor klasszifikáló neuronháló becslése a kapott képen"""
    try:
        return tumor_model.predict(image)
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None


def predict_fracture(image):
    """Törés klasszifikáló neuronháló becslése a kapott képen"""
    try:
        return fracture_model.predict(image)
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None


def preprocess_image(image_file):
    """Képet megfelelő formátumba alakítja a neuronháló számára"""
    try:
        image = Image.open(image_file)
        image = image.convert("RGB")
        image = image.resize((224, 224))
        image = img_to_array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        return image
    except Exception as e:
        print(f"Error preprocessing the image: {e}")
        return None


def classify(type):
    """Tumor illetve törés klasszifikáló neuronháló alkalmazása az API végponton kapott képre"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if 'id' not in request.form:
            return jsonify({'error': 'No id part'}), 401

        id = request.form['id']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 402

        file_bytes = file.read()

        image_proc = io.BytesIO(file_bytes)
        image_save = io.BytesIO(file_bytes)

        image = preprocess_image(image_proc)

        if image is None:
            return jsonify({'error': 'Error processing the image'}), 403


        if type == "tumor":
            prediction_result = predict_tumor(image)
        elif type == "fracture":
            prediction_result = predict_fracture(image)
        else:
            prediction_result = ""
        predicted_class = int(np.argmax(prediction_result, axis=1)[0])
        print(predicted_class)

        confidence = np.max(prediction_result)

        if type == "tumor":
            predicted_label = TUMOR_CLASS_LABELS[predicted_class]
        elif type == "fracture":
            predicted_label = FRACTURE_CLASS_LABELS[predicted_class]
        else:
            predicted_label = ""
        print(predicted_label)

        curr_image_path = insert_image(id, image_save, predicted_label, "prod")

        return jsonify({
            "prediction": predicted_label,
            "confidence": float(confidence),
            "file_path": curr_image_path
        }), 200

    except Exception as e:
        print(f"Error in classification: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500



