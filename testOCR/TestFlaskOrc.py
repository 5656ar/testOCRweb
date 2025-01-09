from flask import Flask, request, render_template, jsonify
import pytesseract
import cv2
import numpy as np
import base64

# กำหนด path ของ Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# ฟังก์ชันสำหรับประมวลผลรูปภาพ
def preprocess_image(image):
    # แปลงรูปภาพเป็นโทนสีเทา
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # เพิ่มความคมชัดด้วย Gaussian Blur
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # เพิ่ม Thresholding เพื่อแยกตัวเลขออกจากพื้นหลัง
    _, threshold_image = cv2.threshold(blurred_image, 120, 255, cv2.THRESH_BINARY_INV)

    return threshold_image

def scan_numbers_from_image(image):
    # Preprocess รูปภาพ
    processed_image = preprocess_image(image)

    # ใช้ Tesseract OCR ตรวจจับตัวเลข
    extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6 -c tessedit_char_whitelist=0123456789')

    # ดึงเฉพาะตัวเลขจากข้อความที่ได้
    numbers = ''.join(filter(str.isdigit, extracted_text))
    return numbers

# หน้าเว็บหลัก
@app.route('/')
def index():
    return render_template('camera.html')

# API สำหรับรับรูปภาพจากเว็บ
@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json.get('image')
    if not data:
        return jsonify({"error": "No image data provided"}), 400

    # แปลง Base64 เป็นรูปภาพ
    image_data = base64.b64decode(data.split(',')[1])
    np_image = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # ตรวจจับตัวเลข
    detected_numbers = scan_numbers_from_image(image)

    return jsonify({"numbers": detected_numbers})

# เริ่มต้น Flask Server
if __name__ == '__main__':
    app.run(debug=True)
