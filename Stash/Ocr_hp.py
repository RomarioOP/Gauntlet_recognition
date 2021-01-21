#Optical image recognition to read hp values based on in game ui settings set to a value of 100
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
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1366, 768))

while(True):
        x = 119
        y = 1000

        ox = 28
        oy = 20
        # screen capture
        img = ImageGrab.grab(bbox=(x, y, x + ox, y + oy))
        img_np = np.array(img)
        scale_percent = 220 # percent of original size
        width = int(img_np.shape[1] * scale_percent / 80)
        height = int(img_np.shape[0] * scale_percent / 80)
        dim = (width, height)


        blur = cv2.bilateralFilter(img_np,9,75,75)
        #noise = cv2.medianBlur( img_np, )
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY )
        #dst = cv2.edgePreservingFilter(gray, flags=1, sigma_s=60, sigma_r=0.4)
        #dst = cv2.detailEnhance(gray, sigma_s=60, sigma_r=0.4)
        frame = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("Screen", frame)
        out.write(frame)
        img_arr = np.array(frame)
        text = pytesseract.image_to_string(frame, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789/')
        text = text.strip()
        if len(text) > 0:
                print(text)
        if cv2.waitKey(1) == 27:
                break

out.release()
cv2.destroyAllWindows()



