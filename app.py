import sqlite3
import re
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image

# Make sure this path is correct for your installation on Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the Flask application
app = Flask(__name__)
DATABASE_PATH = 'database/knowledge_base.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Helper Function to Connect to the Database ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

# --- FINAL, MOST ROBUST CORE LOGIC ---
def process_report_text(report_text):
    """
    Takes raw text, uses a keyword map (including aliases) to find relevant lines,
    and then extracts the value immediately following the keyword.
    """
    normalized_tests = []
    summary_parts = []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Step 1: Build a keyword map from the database.
    # Maps all names and aliases to the canonical test name.
    # e.g., {'hemoglobin': 'Hemoglobin', 'haemoglobin': 'Hemoglobin', 'hgb': 'Hemoglobin'}
    keyword_map = {}
    cursor.execute("SELECT name, aliases FROM tests")
    for row in cursor.fetchall():
        canonical_name = row['name']
        keyword_map[canonical_name.lower()] = canonical_name
        if row['aliases']:
            for alias in row['aliases'].split(','):
                keyword_map[alias.lower().strip()] = canonical_name

    report_lines = report_text.split('\n')
    processed_lines = set() # To avoid processing the same line twice for different aliases

    # Step 2: Go through each line of the report
    for i, line in enumerate(report_lines):
        if i in processed_lines:
            continue

        for keyword, canonical_name in keyword_map.items():
            # Step 3: Check if a keyword is in the line
            if keyword in line.lower():
                # Step 4: Use a context-aware regex to find the number *after* the keyword
                # This prevents grabbing other numbers on the same line (like IDs)
                match = re.search(f'{re.escape(keyword)}[^\d]*([\d\.]+)', line, re.IGNORECASE)
                
                if match:
                    value = float(match.group(1))
                    
                    # We have the name and value, now enrich it with DB info
                    cursor.execute("SELECT * FROM tests WHERE name = ?", (canonical_name,))
                    test_info = cursor.fetchone()
                    
                    if test_info:
                        status = 'normal'
                        ref_low, ref_high = test_info["ref_range_low"], test_info["ref_range_high"]
                        if value < ref_low: status = 'low'
                        elif value > ref_high: status = 'high'
                        
                        if status != 'normal':
                            explanation_key = f"explanation_{status}"
                            test_output = { "name": test_info["name"], "value": value, "unit": test_info["unit"], "status": status, "ref_range": { "low": ref_low, "high": ref_high }, "explanation": test_info[explanation_key] }
                            normalized_tests.append(test_output)
                            summary_parts.append(f"{status.capitalize()} {test_info['name']}")
                        
                        processed_lines.add(i)
                        # We found the test for this line, no need to check other keywords
                        break 
    conn.close()

    if not summary_parts:
        return {"status": "ok", "message": "No abnormal test results found from the known tests list."}
    
    final_summary = "Your report shows: " + " and ".join(summary_parts) + "."
    return {"status": "ok", "tests": normalized_tests, "summary": final_summary}

# --- (The rest of the file is unchanged) ---

@app.route('/simplify-report', methods=['POST'])
def simplify_report_json():
    data = request.get_json()
    if not data or 'report_text' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'report_text' key is required."}), 400
    result = process_report_text(data['report_text'])
    return jsonify(result)

@app.route('/simplify-file', methods=['POST'])
def simplify_report_file():
    if 'report_file' not in request.files: return jsonify({"status": "error", "message": "No file part in the request."}), 400
    file = request.files['report_file']
    if file.filename == '': return jsonify({"status": "error", "message": "No selected file."}), 400
    if file and allowed_file(file.filename):
        try:
            if file.filename.lower().endswith('.txt'):
                extracted_text = file.read().decode('utf-8')
            else:
                image = Image.open(file.stream)
                grayscale_image = image.convert('L')
                threshold_image = grayscale_image.point(lambda x: 0 if x < 140 else 255, '1')
                extracted_text = pytesseract.image_to_string(threshold_image)
        except Exception as e:
            return jsonify({"status": "error", "message": f"Error processing file: {str(e)}"}), 500
        result = process_report_text(extracted_text)
        return jsonify(result)
    return jsonify({"status": "error", "message": "File type not allowed."}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/tests', methods=['POST'])
def add_test():
    data = request.get_json()
    # Updated to check for 'aliases' but not make it strictly required
    required_fields = ['name', 'ref_range_low', 'ref_range_high', 'unit', 'explanation_low', 'explanation_high', 'explanation_normal']
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields."}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tests (name, aliases, ref_range_low, ref_range_high, unit, explanation_low, explanation_high, explanation_normal) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (data['name'], data.get('aliases', ''), data['ref_range_low'], data['ref_range_high'], data['unit'], data['explanation_low'], data['explanation_high'], data['explanation_normal']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Test '{data['name']}' added successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": f"Test '{data['name']}' already exists."}), 409
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)



# import sqlite3
# import re
# import os
# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# import pytesseract
# from PIL import Image

# # Make sure this path is correct for your installation on Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Initialize the Flask application
# app = Flask(__name__)
# DATABASE_PATH = 'database/knowledge_base.db'
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # --- Helper Function to Connect to the Database ---
# def get_db_connection():
#     conn = sqlite3.connect(DATABASE_PATH)
#     conn.row_factory = sqlite3.Row 
#     return conn

# # --- REWRITTEN CORE LOGIC (NEW INTELLIGENT PIPELINE) ---
# def process_report_text(report_text):
#     """
#     Takes raw text, finds lines with known tests from the DB, 
#     and then extracts their values.
#     """
#     normalized_tests = []
#     summary_parts = []
    
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     # Step 1: Get all known test names from our database to use as keywords
#     cursor.execute("SELECT name FROM tests")
#     known_tests = [row['name'] for row in cursor.fetchall()]
    
#     # Split the entire OCR output into individual lines
#     report_lines = report_text.split('\n')
    
#     # Step 2: Go through each line of the report
#     for line in report_lines:
#         # Step 3: Check if the line contains any of our known test names
#         for test_name in known_tests:
#             # Using 'in' is a simple but effective way to find the keyword
#             if test_name.lower() in line.lower():
#                 # We found a relevant line! Now, extract the number from it.
#                 # This simple regex finds the first number (integer or decimal) in the line
#                 value_match = re.search(r'([\d\.]+)', line)
                
#                 if value_match:
#                     value = float(value_match.group(1))
                    
#                     # We have the name and value, now enrich it with DB info
#                     cursor.execute("SELECT * FROM tests WHERE name = ?", (test_name,))
#                     test_info = cursor.fetchone()
                    
#                     status = 'normal'
#                     ref_low, ref_high = test_info["ref_range_low"], test_info["ref_range_high"]

#                     if value < ref_low: status = 'low'
#                     elif value > ref_high: status = 'high'
                    
#                     if status != 'normal':
#                         explanation_key = f"explanation_{status}"
#                         test_output = { "name": test_info["name"], "value": value, "unit": test_info["unit"], "status": status, "ref_range": { "low": ref_low, "high": ref_high }, "explanation": test_info[explanation_key] }
#                         normalized_tests.append(test_output)
#                         summary_parts.append(f"{status.capitalize()} {test_info['name']}")
                    
#                     # Break the inner loop once we've matched and processed a test on this line
#                     break 

#     conn.close()

#     if not summary_parts:
#         return {"status": "ok", "message": "No abnormal test results found from the known tests list."}
    
#     final_summary = "Your report shows: " + " and ".join(summary_parts) + "."
#     return {"status": "ok", "tests": normalized_tests, "summary": final_summary}


# # --- (The rest of the file is unchanged) ---

# # --- Endpoint 1: Handles JSON input ---
# @app.route('/simplify-report', methods=['POST'])
# def simplify_report_json():
#     data = request.get_json()
#     if not data or 'report_text' not in data:
#         return jsonify({"status": "error", "message": "Invalid input. 'report_text' key is required."}), 400
#     result = process_report_text(data['report_text'])
#     return jsonify(result)

# # --- Endpoint 2: Handles File Uploads ---
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/simplify-file', methods=['POST'])
# def simplify_report_file():
#     if 'report_file' not in request.files: return jsonify({"status": "error", "message": "No file part in the request."}), 400
#     file = request.files['report_file']
#     if file.filename == '': return jsonify({"status": "error", "message": "No selected file."}), 400

#     if file and allowed_file(file.filename):
#         try:
#             if file.filename.lower().endswith('.txt'):
#                 extracted_text = file.read().decode('utf-8')
#             else:
#                 image = Image.open(file.stream)
#                 grayscale_image = image.convert('L')
#                 threshold_image = grayscale_image.point(lambda x: 0 if x < 140 else 255, '1')
#                 extracted_text = pytesseract.image_to_string(threshold_image)
#         except Exception as e:
#             return jsonify({"status": "error", "message": f"Error processing file: {str(e)}"}), 500
        
#         result = process_report_text(extracted_text)
#         return jsonify(result)

#     return jsonify({"status": "error", "message": "File type not allowed."}), 400

# # --- Endpoint 3: Add new tests ---
# @app.route('/tests', methods=['POST'])
# def add_test():
#     data = request.get_json()
#     required_fields = ['name', 'ref_range_low', 'ref_range_high', 'unit', 'explanation_low', 'explanation_high', 'explanation_normal']
#     if not all(field in data for field in required_fields):
#         return jsonify({"status": "error", "message": "Missing required fields."}), 400
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO tests (name, ref_range_low, ref_range_high, unit, explanation_low, explanation_high, explanation_normal) VALUES (?, ?, ?, ?, ?, ?, ?)", (data['name'], data['ref_range_low'], data['ref_range_high'], data['unit'], data['explanation_low'], data['explanation_high'], data['explanation_normal']))
#         conn.commit()
#         conn.close()
#         return jsonify({"status": "success", "message": f"Test '{data['name']}' added successfully."}), 201
#     except sqlite3.IntegrityError:
#         return jsonify({"status": "error", "message": f"Test '{data['name']}' already exists."}), 409
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

