import os

# The main directory where the application is located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'knowledge_base.db')
#folder where user_uploaded files will be temporarily stored.
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Path to the Tesseract OCR executable on Windows
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# A set of allowed file extensions for user uploads.
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}

