from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import pytesseract
import cv2
import os

# กำหนด path ของ Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'

def preprocess_image(image_path):
    # โหลดรูปภาพ
    image = cv2.imread(image_path)

    # แปลงรูปภาพเป็นโทนสีเทา
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # เพิ่มความคมชัดด้วย Gaussian Blur
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # เพิ่ม Thresholding เพื่อแยกตัวเลขออกจากพื้นหลัง
    _, threshold_image = cv2.threshold(blurred_image, 120, 255, cv2.THRESH_BINARY_INV)

    return threshold_image

def scan_numbers_from_image(image_path):
    # Preprocess รูปภาพ
    processed_image = preprocess_image(image_path)

    # บันทึกรูปภาพที่ผ่านการปรับปรุง (Debug)
    debug_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.png')
    cv2.imwrite(debug_path, processed_image)

    # ใช้ Tesseract OCR ตรวจจับตัวเลข
    extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6 -c tessedit_char_whitelist=0123456789')

    # ดึงเฉพาะตัวเลขจากข้อความที่ได้
    numbers = ''.join(filter(str.isdigit, extracted_text))
    return numbers, debug_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ตรวจสอบว่ามีการอัปโหลดไฟล์
        if 'image' not in request.files:
            return "No file uploaded", 400

        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400

        # บันทึกรูปภาพ
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # ตรวจจับตัวเลขในรูปภาพ
        detected_numbers, debug_path = scan_numbers_from_image(file_path)

        return render_template('index.html', numbers=detected_numbers, original_image=file.filename, processed_image='processed.png')

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
