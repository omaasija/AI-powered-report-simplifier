import cv2
import numpy as np
import pytesseract
from config import TESSERACT_CMD

# --- Initialization ---
# This line ensures pytesseract knows where to find the Tesseract engine.
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def preprocess_image_for_ocr(image):
    """
    Takes an OpenCV image and applies a preprocessing pipeline to improve OCR accuracy.
    Pipeline includes: Grayscale -> Thresholding -> Deskewing (straightening).
    
    Args:
        image (numpy.ndarray): The image to process in OpenCV format.

    Returns:
        numpy.ndarray: The cleaned, preprocessed image ready for OCR.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # High-contrast black and white conversion
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # --- Deskewing Logic to straighten a tilted image ---
    # This block can cause errors on images with no detectable text.
    # We'll wrap it in a try-except block for robustness.
    try:
        coords = cv2.findNonZero(binary)
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45: angle = -(90 + angle)
        else: angle = -angle
        
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    except cv2.error:
        # If deskewing fails (e.g., blank image), just use the original image.
        rotated = image
    
    # Final cleanup after rotation
    final_gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    final_thresh = cv2.threshold(final_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    return final_thresh

def extract_text_from_image(file_stream):
    """
    Reads an image from an in-memory stream, preprocesses it, and extracts text using OCR.
    
    Args:
        file_stream: The file object from the Flask request.

    Returns:
        str: The extracted text.
    """
    # Read the image file directly from the in-memory stream for efficiency
    image_bytes = np.frombuffer(file_stream.read(), np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    
    # Process the image and perform OCR
    final_image = preprocess_image_for_ocr(image)
    return pytesseract.image_to_string(final_image)

