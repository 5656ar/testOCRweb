import cv2
import pytesseract

# กำหนด path ของ Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def crop_black_rectangle(image_path):
    # โหลดรูปภาพ
    image = cv2.imread(image_path)

    # แปลงเป็นโทนสีเทา
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ใช้ Threshold เพื่อตรวจจับพื้นที่สีดำ
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # หาขอบเขตของวัตถุในภาพ
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # คำนวณกรอบสี่เหลี่ยมรอบพื้นที่ที่ตรวจจับได้
        x, y, w, h = cv2.boundingRect(contour)

        # เงื่อนไข: กรองเฉพาะพื้นที่ที่มีขนาดใกล้เคียงตัวเลขในกรอบสีดำ
        if 100 < w < 500 and 30 < h < 200:  # ปรับค่าตามรูปภาพ
            cropped = image[y:y+h, x:x+w]
            return cropped  # คืนค่าภาพที่ถูกตัด

    return None

def detect_numbers_from_cropped_image(cropped_image):
    # แปลงเป็นโทนสีเทา
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # ใช้ Thresholding
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    # ใช้ Tesseract OCR
    extracted_text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789')

    # ดึงเฉพาะตัวเลข
    numbers = ''.join(filter(str.isdigit, extracted_text))
    return numbers

# เส้นทางรูปภาพ
image_path = 'pic/test1111.jpg'

# ตัดเฉพาะตัวเลขในกรอบสีดำ
cropped_image = crop_black_rectangle(image_path)

if cropped_image is not None:
    # แสดงภาพที่ถูกตัด
    cv2.imshow("Cropped Image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ตรวจจับตัวเลข
    detected_numbers = detect_numbers_from_cropped_image(cropped_image)
    print("Detected Numbers:", detected_numbers)
else:
    print("No black rectangle found!")
