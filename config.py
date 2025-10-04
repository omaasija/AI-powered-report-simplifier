import os

# --- File System Paths ---
# The main directory where the application is located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to the SQLite database file.
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'knowledge_base.db')
# Folder where user-uploaded files will be temporarily stored.
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# --- Tesseract OCR Configuration ---
# On Windows, you must provide the full path to the Tesseract executable.
# On macOS and Linux (if installed via a package manager like Homebrew or apt),
# you can often leave this as just 'tesseract'.
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- Application Settings ---
# A set of allowed file extensions for user uploads.
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}

