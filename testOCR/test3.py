from PIL import Image
import pytesseract
import cv2

# กำหนด path ของ Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

    # แสดงรูปภาพหลังการปรับปรุง (สำหรับ Debug)
    cv2.imshow("Processed Image", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ใช้ Tesseract OCR ตรวจจับตัวเลข
    extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6 -c tessedit_char_whitelist=0123456789')

    # ดึงเฉพาะตัวเลขจากข้อความที่ได้
    numbers = ''.join(filter(str.isdigit, extracted_text))
    return numbers

# ระบุเส้นทางรูปภาพ
image_path = "pic/test27.JPG"
detected_numbers = scan_numbers_from_image(image_path)

if detected_numbers:
    print("Detected numbers:", detected_numbers)
else:
    print("No numbers detected.")
