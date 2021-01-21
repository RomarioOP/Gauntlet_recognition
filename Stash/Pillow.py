#Draft ocr
import cv2
import numpy as np
import pytesseract

# We only need the ImageGrab class from PIL
from PIL import ImageGrab
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# Run forever unless you press Esc
while True:
    # This instance will generate an image from
    # the point of (115, 143) and (569, 283) in format of (x, y)
    img = ImageGrab.grab(bbox=(115, 1000, 569, 1283))
    img_arr = np.array(img)
    cv2.imshow("", img_arr)

    
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)

    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    out_below = pytesseract.image_to_string(img)


    text = pytesseract.image_to_string(img)
    text = text.strip()
    if len(text) > 0:
        print(text)

    # This line will break the while loop when you press Esc
    if cv2.waitKey(1) == 27:
        break

# This will make sure all windows created from cv2 is destroyed
cv2.destroyAllWindows()