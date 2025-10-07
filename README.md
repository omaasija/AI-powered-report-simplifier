🔬 AI-Powered Medical Report Simplifier

This backend service provides a robust API to parse medical lab reports (from text or images), analyze the results against a dynamic knowledge base, and return patient-friendly explanations. The project is built with Python and Flask and is deployed on Render.

🚀 Live Demo URL: https://ai-powered-report-simplifier.onrender.com
✨ Key Features

    ✅ Multi-Format Input: Handles raw text (JSON), .txt files, and image files (.png, .jpg).

    ✅ Advanced OCR Pipeline: Uses OpenCV for a professional-grade image preprocessing pipeline (grayscale, thresholding, and auto-straightening/deskewing) before sending the image to Tesseract for highly accurate text extraction.

    ✅ Intelligent, Context-Aware Analysis: The "brain" of the application uses a keyword-driven approach to filter out noise (like Patient IDs or dates) and accurately extracts only the relevant medical test values.

    ✅ Dynamic Knowledge Base: The system's medical knowledge is completely decoupled from the code. New tests, spelling variations, and aliases (WBC vs. White Blood Cell Count) can be added at any time via a dedicated API endpoint without ever touching the core logic.

    ✅ Robust Error Handling: Implements clear guardrails for invalid inputs, disallowed file types, and internal server errors, always returning a clean JSON response.

🏛️ Tech Stack & Architecture

The application is built using a modular, service-oriented architecture to separate concerns and improve maintainability. This clean structure allows for easy updates and scalability.

File
	

Role

app.py
	

Main Controller: Initializes the Flask server and defines all API routes. Orchestrates the flow by calling the other modules.

config.py
	

Configuration: A centralized file for all settings, like database paths and the Tesseract command path.

database_utils.py
	

Database Module: Handles all direct interactions with the SQLite database.

image_processor.py
	

Image Processing Module: Contains the advanced OpenCV and Tesseract OCR pipeline for extracting text from images.

report_analyzer.py
	

Analysis Engine: The "brain" of the application. Contains the core logic for parsing text and analyzing results.

setup_database.py
	

Utility Script: Creates and populates the knowledge_base.db from a master data list, making the knowledge base easy to manage.
⚙️ Getting Started (Local Development)

Follow these steps to set up and run the project on your local machine.

    Clone the Repository

    git clone <your-repo-url.git>
    cd <your-repo-name>

    Create and Activate a Virtual Environment

    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    .\venv\Scripts\activate   # On Windows

    Install Dependencies

    pip install -r requirements.txt

    (Windows Only) Install Tesseract

        Ensure the Tesseract OCR engine is installed and that the path in config.py is correct.

    Set Up the Database

    python setup_database.py

    Run the Server

    python app.py

        The server will be running at http://localhost:5000.

🔌 API Endpoints
1. Simplify a Report from a File

Upload a .txt, .png, or .jpg file containing a medical report for analysis.

    Endpoint: POST /simplify-file

    Postman Setup:

        URL: https://ai-powered-report-simplifier.onrender.com/simplify-file

        Body: form-data

        Key: report_file

        Type: File

2. Add a New Test to the Knowledge Base

Dynamically add a new medical test to the application's database.

    Endpoint: POST /tests

    Request Body (application/json):

    {
        "name": "Glucose",
        "aliases": "blood sugar",
        "ref_range_low": 70,
        "ref_range_high": 100,
        "unit": "mg/dL",
        "explanation_low": "Low glucose (hypoglycemia) can cause dizziness.",
        "explanation_high": "High glucose (hyperglycemia) is a sign of diabetes.",
        "explanation_normal": "Your blood sugar is in the normal range."
    }

