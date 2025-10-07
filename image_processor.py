import cv2
import numpy as np
import pytesseract
import pandas as pd 
from config import TESSERACT_CMD

#initialize tesseract cmd path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def preprocess_image_for_ocr(image):
    #preprocess the image for better ocr results

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
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
        rotated = image
    final_gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    final_thresh = cv2.threshold(final_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return final_thresh

def extract_text_and_confidence_from_image(file_stream):
   #read image
   #preprocess image
   #perform ocr and get confidence score
    image_bytes = np.frombuffer(file_stream.read(), np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Could not decode the image file. It may be corrupted.")

    final_image = preprocess_image_for_ocr(image)
    
   
    # The output_type is set to DATAFRAME to make it easy to work with pandas
    
    ocr_data = pytesseract.image_to_data(final_image, output_type=pytesseract.Output.DATAFRAME)
    
    # Filter out non-textual elements (where confidence is -1)
    ocr_data = ocr_data[ocr_data.conf != -1]
    
    # Calculate the average confidence of the recognized words
    if not ocr_data.empty:
        average_confidence = ocr_data['conf'].mean() / 100.0
    else:
        average_confidence = 0.0

    # Reconstruct the full text from the image
    extracted_text = pytesseract.image_to_string(final_image)
    
    return extracted_text, average_confidence

