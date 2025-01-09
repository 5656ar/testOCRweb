from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename

import pytesseract
import cv2

# กำหนด path ของ Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, threshold_image = cv2.threshold(blurred_image, 120, 255, cv2.THRESH_BINARY_INV)
    return threshold_image

def scan_numbers_from_image(image_path):
    processed_image = preprocess_image(image_path)
    extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6 -c tessedit_char_whitelist=0123456789')
    numbers = ''.join(filter(str.isdigit, extracted_text))
    return numbers

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    detected_numbers = scan_numbers_from_image(file_path)
    os.remove(file_path)  # Optional: Remove file after processing

    return jsonify({"numbers": detected_numbers or "No numbers detected"})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
