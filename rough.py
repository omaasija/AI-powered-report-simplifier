# Step 1: Set the Request Method and URL

#     Open a new tab in Postman.

#     Change the HTTP Method from GET to POST.

#     In the URL bar, enter the address for your file upload endpoint:
#     http://127.0.0.1:5000/simplify-file

# Step 2: Configure the Request Body for File Upload

#     Click on the Body tab below the URL bar.

#     Select the form-data radio button. This is the correct type for sending files.

# Step 3: Attach the File

#     A table of Key-Value pairs will appear. In the first row, under the KEY column, type the name your Flask app is expecting: report_file. (This must be spelled exactly right).

#     Hover your mouse over the KEY cell you just typed in. On the right side, a dropdown menu will appear that says "Text". Click it and select "File".

#     The VALUE column will now change to a button that says "Select Files". Click this button.

#     A file browser window will open. Navigate to and select the .txt or image file (e.g., sample_report.txt or report_image.png) you want to upload.




# # import sqlite3
# # import re
# # import os
# # from flask import Flask, request, jsonify
# # from werkzeug.utils import secure_filename
# # # --- New Imports for OCR ---
# # import pytesseract
# # from PIL import Image

# # # --- Add this line if you installed Tesseract in a non-standard location on Windows ---
# # # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # # Initialize the Flask application
# # app = Flask(__name__)
# # DATABASE_PATH = 'database/knowledge_base.db'
# # UPLOAD_FOLDER = 'uploads'
# # ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # # --- Helper Function to Connect to the Database ---
# # def get_db_connection():
# #     conn = sqlite3.connect(DATABASE_PATH)
# #     conn.row_factory = sqlite3.Row 
# #     return conn

# # # --- REFACTORED CORE LOGIC ---
# # def process_report_text(report_text):
# #     """Takes raw text and returns the simplified report data."""
# #     test_pattern = re.compile(r"([a-zA-Z\s]+?)\s*:\s*([\d\.]+)", re.IGNORECASE)
# #     found_tests = test_pattern.finditer(report_text)
    
# #     normalized_tests = []
# #     summary_parts = []
    
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
    
# #     for match in found_tests:
# #         name = match.group(1).strip()
# #         value = float(match.group(2))
        
# #         cursor.execute("SELECT * FROM tests WHERE name LIKE ?", (f"%{name}%",))
# #         test_info = cursor.fetchone()
        
# #         if test_info:
# #             status = ''
# #             ref_low = test_info["ref_range_low"]
# #             ref_high = test_info["ref_range_high"]

# #             if value < ref_low: status = 'low'
# #             elif value > ref_high: status = 'high'
# #             else: status = 'normal'
            
# #             if status != 'normal':
# #                 explanation_key = f"explanation_{status}"
# #                 test_output = { "name": test_info["name"], "value": value, "unit": test_info["unit"], "status": status, "ref_range": { "low": ref_low, "high": ref_high }, "explanation": test_info[explanation_key] }
# #                 normalized_tests.append(test_output)
# #                 summary_parts.append(f"{status.capitalize()} {test_info['name']}")

# #     conn.close()

# #     if not summary_parts:
# #         return {"status": "ok", "message": "All test results are within the normal range."}
    
# #     final_summary = "Your report shows: " + " and ".join(summary_parts) + "."
# #     return {"status": "ok", "tests": normalized_tests, "summary": final_summary}


# # # --- Endpoint 1: Handles JSON input (Now simpler) ---
# # @app.route('/simplify-report', methods=['POST'])
# # def simplify_report_json():
# #     data = request.get_json()
# #     if not data or 'report_text' not in data:
# #         return jsonify({"status": "error", "message": "Invalid input. 'report_text' key is required."}), 400
    
# #     # Call the reusable logic function
# #     result = process_report_text(data['report_text'])
# #     return jsonify(result)

# # # --- Endpoint 2: Handles File Uploads (NEW) ---
# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # @app.route('/simplify-file', methods=['POST'])
# # def simplify_report_file():
# #     if 'report_file' not in request.files:
# #         return jsonify({"status": "error", "message": "No file part in the request."}), 400
    
# #     file = request.files['report_file']
# #     if file.filename == '':
# #         return jsonify({"status": "error", "message": "No selected file."}), 400

# #     if file and allowed_file(file.filename):
# #         filename = secure_filename(file.filename)
# #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #         file.save(filepath)
        
# #         extracted_text = ""
# #         try:
# #             if filename.lower().endswith('.txt'):
# #                 with open(filepath, 'r') as f:
# #                     extracted_text = f.read()
# #             else: # It's an image
# #                 extracted_text = pytesseract.image_to_string(Image.open(filepath))
# #         except Exception as e:
# #             return jsonify({"status": "error", "message": f"Error processing file: {str(e)}"}), 500
        
# #         # Call the reusable logic function with the extracted text
# #         result = process_report_text(extracted_text)
# #         return jsonify(result)

# #     return jsonify({"status": "error", "message": "File type not allowed."}), 400

# # # Endpoint to add new tests remains the same
# # @app.route('/tests', methods=['POST'])
# # def add_test():
# #     # ... (code for this function is unchanged) ...
# #     data = request.get_json()
# #     required_fields = ['name', 'ref_range_low', 'ref_range_high', 'unit', 'explanation_low', 'explanation_high', 'explanation_normal']
# #     if not all(field in data for field in required_fields): return jsonify({"status": "error", "message": "Missing required fields."}), 400
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
# #         cursor.execute("INSERT INTO tests (name, ref_range_low, ref_range_high, unit, explanation_low, explanation_high, explanation_normal) VALUES (?, ?, ?, ?, ?, ?, ?)", (data['name'], data['ref_range_low'], data['ref_range_high'], data['unit'], data['explanation_low'], data['explanation_high'], data['explanation_normal']))
# #         conn.commit()
# #         conn.close()
# #         return jsonify({"status": "success", "message": f"Test '{data['name']}' added successfully."}), 201
# #     except sqlite3.IntegrityError: return jsonify({"status": "error", "message": f"Test '{data['name']}' already exists."}), 409
# #     except Exception as e: return jsonify({"status": "error", "message": str(e)}), 500

# # if __name__ == '__main__':
# #     app.run(debug=True, port=5000)


# #     import sqlite3
# # import re
# # import os
# # from flask import Flask, request, jsonify
# # from werkzeug.utils import secure_filename
# # # --- New Imports for OCR and File Handling ---
# # import pytesseract
# # from PIL import Image

# # # --- Add this line if you installed Tesseract in a non-standard location on Windows ---
# # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # # Initialize the Flask application
# # app = Flask(__name__)
# # DATABASE_PATH = 'database/knowledge_base.db'
# # # --- New Configuration for File Uploads ---
# # UPLOAD_FOLDER = 'uploads'
# # ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # Create the upload folder if it doesn't exist
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# # # --- Helper Function to Connect to the Database ---
# # def get_db_connection():
# #     """Establishes a connection to the SQLite database."""
# #     conn = sqlite3.connect(DATABASE_PATH)
# #     conn.row_factory = sqlite3.Row 
# #     return conn

# # # --- REFACTORED CORE LOGIC FUNCTION ---
# # def process_report_text(report_text):
# #     """
# #     This function contains the core analysis logic. It takes raw text as input
# #     and returns a dictionary with the simplified report. It is now reusable.
# #     """
# #     test_pattern = re.compile(r"([a-zA-Z\s]+?)\s*:\s*([\d\.]+)", re.IGNORECASE)
# #     found_tests = test_pattern.finditer(report_text)
    
# #     normalized_tests = []
# #     summary_parts = []
    
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
    
# #     for match in found_tests:
# #         name = match.group(1).strip()
# #         value = float(match.group(2))
        
# #         cursor.execute("SELECT * FROM tests WHERE name LIKE ?", (f"%{name}%",))
# #         test_info = cursor.fetchone()
        
# #         if test_info:
# #             status = 'normal'
# #             ref_low, ref_high = test_info["ref_range_low"], test_info["ref_range_high"]

# #             if value < ref_low: status = 'low'
# #             elif value > ref_high: status = 'high'
            
# #             if status != 'normal':
# #                 explanation_key = f"explanation_{status}"
# #                 test_output = {
# #                     "name": test_info["name"], "value": value, "unit": test_info["unit"],
# #                     "status": status,
# #                     "ref_range": { "low": ref_low, "high": ref_high },
# #                     "explanation": test_info[explanation_key]
# #                 }
# #                 normalized_tests.append(test_output)
# #                 summary_parts.append(f"{status.capitalize()} {test_info['name']}")

# #     conn.close()

# #     if not summary_parts:
# #         return {"status": "ok", "message": "All test results are within the normal range."}
    
# #     final_summary = "Your report shows: " + " and ".join(summary_parts) + "."
# #     return {"status": "ok", "tests": normalized_tests, "summary": final_summary}


# # # A simple route to test if the server is running
# # @app.route('/')
# # def index():
# #     return "Medical Report Simplifier API is running!"

# # # Endpoint 1: Your original endpoint for JSON text, now uses the refactored function
# # @app.route('/simplify-report', methods=['POST'])
# # def simplify_report_json():
# #     data = request.get_json()
# #     if not data or 'report_text' not in data:
# #         return jsonify({"status": "error", "message": "Invalid input. 'report_text' key is required."}), 400
    
# #     # Call the reusable logic function
# #     result = process_report_text(data['report_text'])
# #     return jsonify(result)

# # # --- Endpoint 2: NEW ENDPOINT FOR FILE UPLOADS ---
# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # @app.route('/simplify-file', methods=['POST'])
# # def simplify_report_file():
# #     if 'report_file' not in request.files:
# #         return jsonify({"status": "error", "message": "No file part in the request."}), 400
    
# #     file = request.files['report_file']
# #     if file.filename == '':
# #         return jsonify({"status": "error", "message": "No selected file."}), 400

# #     if file and allowed_file(file.filename):
# #         filename = secure_filename(file.filename)
# #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #         file.save(filepath)
        
# #         extracted_text = ""
# #         try:
# #             if filename.lower().endswith('.txt'):
# #                 with open(filepath, 'r') as f:
# #                     extracted_text = f.read()
# #             else: # It's an image, so use Pytesseract
# #                 extracted_text = pytesseract.image_to_string(Image.open(filepath))
# #         except Exception as e:
# #             return jsonify({"status": "error", "message": f"Error processing file: {str(e)}"}), 500
        
# #         # Call the reusable logic function with the extracted text
# #         result = process_report_text(extracted_text)
# #         return jsonify(result)

# #     return jsonify({"status": "error", "message": "File type not allowed."}), 400

# # # Endpoint 3: Your endpoint to add new tests (unchanged)
# # @app.route('/tests', methods=['POST'])
# # def add_test():
# #     data = request.get_json()
# #     required_fields = ['name', 'ref_range_low', 'ref_range_high', 'unit', 'explanation_low', 'explanation_high', 'explanation_normal']
# #     if not all(field in data for field in required_fields):
# #         return jsonify({"status": "error", "message": "Missing required fields."}), 400
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
# #         cursor.execute("INSERT INTO tests (name, ref_range_low, ref_range_high, unit, explanation_low, explanation_high, explanation_normal) VALUES (?, ?, ?, ?, ?, ?, ?)", (data['name'], data['ref_range_low'], data['ref_range_high'], data['unit'], data['explanation_low'], data['explanation_high'], data['explanation_normal']))
# #         conn.commit()
# #         conn.close()
# #         return jsonify({"status": "success", "message": f"Test '{data['name']}' added successfully."}), 201
# #     except sqlite3.IntegrityError:
# #         return jsonify({"status": "error", "message": f"Test '{data['name']}' already exists."}), 409
# #     except Exception as e:
# #         return jsonify({"status": "error", "message": str(e)}), 500

# # # This allows you to run the app directly from the command line
# # if __name__ == '__main__':
# #     app.run(debug=True, port=5000)
