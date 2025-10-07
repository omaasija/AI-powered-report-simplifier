import os
import sqlite3
from flask import Flask, request, jsonify

# --- Import custom modules ---
from config import ALLOWED_EXTENSIONS
# The image processor now returns two values
from image_processor import extract_text_and_confidence_from_image
# The report analyzer now returns three values
from report_analyzer import normalize_tests, generate_summary, generate_final_output

# --- Initialization ---
app = Flask(__name__)

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- NEW STEP-BY-STEP API ENDPOINTS ---

@app.route('/step1/extract', methods=['POST'])
def step1_extract_text():
    """
    Step 1: Handles text or image input and returns the raw extracted text lines
    with a dynamically calculated confidence score.
    """
    if 'report_file' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request."}), 400

    file = request.files['report_file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file."}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "File type not allowed."}), 400

    try:
        ocr_confidence = 1.0 # Default confidence for text files is 100%
        if file.filename.lower().endswith('.txt'):
            extracted_text = file.read().decode('utf-8')
        else:
            # This function now returns both the text and a confidence score
            extracted_text, ocr_confidence = extract_text_and_confidence_from_image(file)

        # We still call normalize_tests to get the raw lines it identified
        raw_lines, _, _ = normalize_tests(extracted_text)

        return jsonify({
            "tests_raw": raw_lines,
            "confidence": round(ocr_confidence, 2) # Use the dynamic score
           
        })

    except Exception as e:
        print(f"!!! An error occurred in Step 1: {e}")
        return jsonify({"status": "error", "message": "An error occurred during text extraction."}), 500

@app.route('/step2/normalize', methods=['POST'])
def step2_normalize_data():
    """
    Step 2: Takes raw text and returns the normalized JSON with a dynamic
    normalization confidence score.
    """
    data = request.get_json()
    if not data or 'full_text' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'full_text' from Step 1 is required."}), 400

    # This function now returns a third value: the normalization confidence
    _, normalized_data, norm_confidence = normalize_tests(data['full_text'])

    return jsonify({
        "tests": normalized_data,
        "normalization_confidence": round(norm_confidence, 2) # Use the dynamic score
    })

@app.route('/step3/summarize', methods=['POST'])
def step3_get_summary():
    """
    Step 3: Takes the normalized test data from Step 2 and returns the patient-friendly summary.
    """
    data = request.get_json()
    if not data or 'tests' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'tests' array from Step 2 is required."}), 400

    summary_data = generate_summary(data['tests'])
    return jsonify(summary_data)

@app.route('/step4/finalize', methods=['POST'])
def step4_get_final_output():
    """
    Step 4: Takes the normalized test data from Step 2 and returns the final, clean output.
    """
    data = request.get_json()
    if not data or 'tests' not in data:
        return jsonify({"status": "error", "message": "Invalid input. 'tests' array from Step 2 is required."}), 400

    final_data = generate_final_output(data['tests'])
    return jsonify(final_data)

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

