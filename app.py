import os
import sqlite3
from flask import Flask, request, jsonify

# --- Import custom modules ---
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from database_utils import get_db_connection
from image_processor import extract_text_from_image
from report_analyzer import process_report_text

# --- Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Helper Function ---
def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- API Endpoints ---

@app.route('/simplify-report', methods=['POST'])
def simplify_report_json():
    """Endpoint for simplifying a report from a raw text JSON payload."""
    data = request.get_json()
    if not data or 'report_text' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'report_text' key is required."}), 400
    
    result = process_report_text(data['report_text'])
    return jsonify(result)

@app.route('/simplify-file', methods=['POST'])
def simplify_report_file():
    """Endpoint for simplifying a report from an uploaded file (text or image)."""
    if 'report_file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request."}), 400
    
    file = request.files['report_file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file."}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "File type not allowed."}), 400
        
    try:
        if file.filename.lower().endswith('.txt'):
            extracted_text = file.read().decode('utf-8')
        else:
            extracted_text = extract_text_from_image(file)

        result = process_report_text(extracted_text)
        return jsonify(result)

    except Exception as e:
        print(f"!!! An error occurred processing a file: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred while processing the file."}), 500

@app.route('/tests', methods=['POST'])
def add_test():
    """Endpoint for adding a new test to the knowledge base."""
    data = request.get_json()
    required_fields = ['name', 'ref_range_low', 'ref_range_high', 'unit', 'explanation_low', 'explanation_high', 'explanation_normal']
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing one or more required fields."}), 400
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tests (name, aliases, ref_range_low, ref_range_high, unit, explanation_low, explanation_high, explanation_normal) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['name'], data.get('aliases', ''), data['ref_range_low'], 
            data['ref_range_high'], data['unit'], data['explanation_low'], 
            data['explanation_high'], data['explanation_normal']
        ))
        conn.commit()
        return jsonify({"status": "success", "message": f"Test '{data['name']}' added successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": f"Test '{data['name']}' already exists."}), 409
    except sqlite3.Error as e:
        print(f"Database error adding test: {e}")
        return jsonify({"status": "error", "message": "A database error occurred."}), 500
    finally:
        if conn:
            conn.close()

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

