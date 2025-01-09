from PIL import Image
import pytesseract
import cv2

# กำหนด path ของ Tesseract OCR (เปลี่ยนตามระบบของคุณ)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def invert_image(image):
    return cv2.bitwise_not(image)
# ฟังก์ชันสำหรับสแกนตัวเลขจากรูปภาพ
def scan_numbers_from_image(image_path):
    # โหลดรูปภาพ
    image = cv2.imread("pic/test6.JPG")
    
    # แปลงรูปภาพเป็นโทนสีเทาเพื่อเพิ่มความแม่นยำ
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = invert_image(gray_image)
    
    # ใช้ Tesseract OCR เพื่อดึงข้อความจากรูปภาพ
    extracted_text = pytesseract.image_to_string(inverted_image, config='--psm 6 digits')
    cv2.imshow("Threshold Image", inverted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # ดึงเฉพาะตัวเลขจากข้อความที่ได้
    numbers = ''.join(filter(str.isdigit, extracted_text))
    return numbers

# ตัวอย่างการใช้งาน
image_path = 'example_image_with_numbers.jpg'  # ระบุ path ของรูปภาพ
detected_numbers = scan_numbers_from_image(image_path)

if detected_numbers:
    print("Detected numbers:", detected_numbers)
else:
    print("No numbers detected.")
