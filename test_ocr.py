# import cv2
# import numpy as np
# import pytesseract
# from PIL import Image

# # IMPORTANT: Make sure this path is correct for your Windows installation
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def preprocess_image_for_ocr(image_path):
#     """A simplified version of your preprocessing pipeline for testing."""
#     try:
#         image = cv2.imread(image_path)
#         if image is None:
#             print("!!! ERROR: Image not found or could not be read. Check the path.")
#             return None
        
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         # Using a simple threshold for testing
#         _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#         print("--- Image preprocessing complete. ---")
#         return binary
#     except Exception as e:
#         print(f"!!! ERROR during preprocessing: {e}")
#         return None

# def run_ocr_test():
#     image_path = 'golden_img.png'
#     print(f"--- Starting OCR test on '{image_path}' ---")
    
#     # Preprocess the image
#     processed_image = preprocess_image_for_ocr(image_path)
    
#     if processed_image is not None:
#         try:
#             # Perform OCR
#             extracted_text = pytesseract.image_to_string(processed_image)
            
#             print("\n--- OCR RAW OUTPUT ---")
#             print(f"'{extracted_text.strip()}'")
#             print("----------------------")

#             if "hemoglobin" in extracted_text.lower():
#                 print("\n✅ SUCCESS: The script correctly identified 'hemoglobin'.")
#             else:
#                 print("\n❌ FAILURE: The script ran, but the OCR output did not contain the expected text.")

#         except pytesseract.TesseractNotFoundError:
#             print("\n❌ CRITICAL FAILURE: Tesseract is not installed or not in your PATH.")
#             print("   Please install Tesseract or fix the path in the script.")
#         except Exception as e:
#             print(f"\n!!! ERROR during OCR: {e}")

# if __name__ == '__main__':
#     run_ocr_test()

# # python test_ocr.py

