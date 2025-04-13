from flask import Blueprint, request, jsonify
from dicom2jpg import dicom2jpg
import tempfile
import os
from Model import config
import shutil

convert_bp = Blueprint('convert', __name__)

@convert_bp.route('/convert', methods=['POST'])
def convert():
    """Képek jpg formátumba való konvertálását végzi"""

    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']

        temp_file_path = save_uploaded_file(file)
        temp_dir = os.path.join(config.BASE_PATH, "temp_files")
        jpg_file_path = convert_dicom_to_jpg(temp_file_path, temp_dir)

        return jsonify({
            "jpg_file_path": jpg_file_path
        }), 200

    except Exception as e:
        print(f"Error in converting: {e}")
        return jsonify({'error': 'An error occurred during converting'}), 500


def save_uploaded_file(uploaded_file):
    """Temporálisan elmenti a feltöltött képet"""
    try:
        temp_file_path = tempfile.mktemp(suffix='.dcm')
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        return temp_file_path
    except Exception as e:
        print(f"Error in saving: {e}")


def convert_dicom_to_jpg(dicom_file_path, output_dir):
    """DICOM képet átkonvertálja JPG kiterjesztésű képpé"""
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        dicom2jpg(dicom_file_path, output_dir)

        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".jpg"):
                    return os.path.join(root, file)
    except Exception as e:
        print(f"Error in converting: {e}")
