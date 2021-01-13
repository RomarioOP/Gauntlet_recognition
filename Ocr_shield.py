#Optical image recognition to read shield values based on in game ui settings set to a value of 100
from PIL import ImageGrab
from PIL import Image
import numpy as np
import pytesseract
import argparse
import cv2
import os
import string
import re
#https://www.learnopencv.com/non-photorealistic-rendering-using-opencv-python-c/
#https://stackoverflow.com/questions/52899174/real-time-ocr-in-python
#https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/?completed=/mog-background-reduction-python-opencv-tutorial/
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1366, 768))

while(True):
        x = 145
        y = 965

        ox = 20
        oy = 17
        # screen capture
        img = ImageGrab.grab(bbox=(x, y, x + ox, y + oy))
        img_np = np.array(img)
        scale_percent = 220 # percent of original size
        width = int(img_np.shape[1] * scale_percent / 80)
        height = int(img_np.shape[0] * scale_percent / 80)
        dim = (width, height)

        blur = cv2.bilateralFilter(img_np,15,75,75)
        #blur = cv2.bilateralFilter(img_np,9,75,75)
        #noise = cv2.medianBlur( img_np, 1)
        #gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV_FULL)
        #dst = cv2.edgePreservingFilter(gray, flags=1, sigma_s=60, sigma_r=0.4)
        #dst = cv2.detailEnhance(gray, sigma_s=60, sigma_r=0.4)
        frame = cv2.resize(blur, dim, interpolation = cv2.INTER_AREA)
        #frame=blur
        cv2.imshow("Screen", frame)
        out.write(frame)
        img_arr = np.array(frame)
        text = pytesseract.image_to_string(frame, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789/n')
        text = text.strip()

        #ocr_result = pytesseract.image_to_string(frame, lang='eng', boxes=False, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

        
        if len(text) > 0:
            if "n" in text:
                text = "11"
                print(text)
            elif "163" in text:
                text = "16"
                print(text)
            else:
                print (text)



        if cv2.waitKey(1) == 27:
                break

out.release()
cv2.destroyAllWindows()



