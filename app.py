import os
import sqlite3
from flask import Flask, request, jsonify

from config import ALLOWED_EXTENSIONS

# The image processor now returns two values
from image_processor import extract_text_and_confidence_from_image

# The report analyzer now returns three values
from report_analyzer import normalize_tests, generate_summary, generate_final_output

# initialization
app = Flask(__name__)

def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#all api endpoints
@app.route('/', methods=['GET'])
def index():
    """A simple welcome route to confirm the API is running."""
    return jsonify({
        "status": "ok",
        "message": "AI-Powered Medical Report Simplifier API is running."
    })

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


@app.route('/simplify-report-final', methods=['POST'])
def simplify_report_final_output():
    #take the img or txt as input and return the final output json
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

       #normalize the extracted text 
        _, normalized_data, _ = normalize_tests(extracted_text)
        
        #generate the final output
        final_result = generate_final_output(normalized_data)
        
        return jsonify(final_result)

    except Exception as e:
        print(f"!!! An error occurred processing a file: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred while processing the file."}), 500
    
@app.route('/step1/extract', methods=['POST'])
def step1_extract_text():
   #take img or txt file and return the extracted text with a dynamic ocr confidence score
    if 'report_file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request."}), 400

    file = request.files['report_file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file."}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "File type not allowed."}), 400

    try:
        ocr_confidence = 1.0 #default confidence for text files
        if file.filename.lower().endswith('.txt'):
            extracted_text = file.read().decode('utf-8')
        else:
           #returns both the extracted text and the confidence score
            extracted_text, ocr_confidence = extract_text_and_confidence_from_image(file)

      #normalize the extracted text to get the raw lines for output
        raw_lines, _, _ = normalize_tests(extracted_text)

        return jsonify({
            "tests_raw": raw_lines,
            "confidence": round(ocr_confidence, 2) 
           
        })

    except Exception as e:
        print(f"!!! An error occurred in Step 1: {e}")
        return jsonify({"status": "error", "message": "An error occurred during text extraction."}), 500

@app.route('/step2/normalize', methods=['POST'])
def step2_normalize_data():
  #take raw text from step 1 and return the normalized test data
  #  with a dynamic normalization confidence score
    data = request.get_json()
    if not data or 'full_text' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'full_text' from Step 1 is required."}), 400

    #returns three values, we only need the second and third
    _, normalized_data, norm_confidence = normalize_tests(data['full_text'])

    return jsonify({
        "tests": normalized_data,
        "normalization_confidence": round(norm_confidence, 2) # Use the dynamic score
    })

@app.route('/step3/summarize', methods=['POST'])
def step3_get_summary():
   #take the normalized test data from Step 2 and return the patient-friendly summary
    data = request.get_json()
    if not data or 'tests' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'tests' array from Step 2 is required."}), 400

    summary_data = generate_summary(data['tests'])
    return jsonify(summary_data)

@app.route('/step4/finalize', methods=['POST'])
def step4_get_final_output():
   #take the normalized test data from Step 2 and return the final output json
    data = request.get_json()
    if not data or 'tests' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'tests' array from Step 2 is required."}), 400

    final_data = generate_final_output(data['tests'])
    return jsonify(final_data)

#main execution
if __name__ == '__main__':
    app.run(debug=True, port=5000)

