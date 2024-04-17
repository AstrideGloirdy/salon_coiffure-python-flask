# file_manager.py
import os
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER


def save_uploaded_file(fichier):
    if fichier:
        filename = secure_filename(fichier.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        fichier.save(file_path)
        return filename
    return None