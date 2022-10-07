import numpy as np
import cv2 
import urllib.request
import sys
import pyocr
import time
from PIL import Image
import pyocr.builders
import pytesseract

path = ""

sys.tracebacklimit = 0

tools = pyocr.get_available_tools()
tool = tools[0]

#langs = tool.get_available_languages()
#print("{}" .format(" ".join(langs)))

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


url = 'http://192.168.50.197:9601/stream'
CAMERA_NAME = 'IP CAMERA TEST'
CAMERA_BUFFER_SIZE = 4096
stream = urllib.request.urlopen(url)
bts = b''



while True:
    bts += stream.read(CAMERA_BUFFER_SIZE)
    a = bts.find(b'\xff\xd8')
    b = bts.find(b'\xff\xd9')
    if a > -1 and b > -1:
        jpg = bts[a:b + 2]
        bts = bts[b + 2:]
        img = cv2.imdecode(np.frombuffer(jpg, dtype = np.uint8), cv2.IMREAD_UNCHANGED)
        vertical_img = cv2.flip(img, 0)
        parallel_img = cv2.flip(img, 1)
        pa_Ver_img = cv2.flip(img, -1)
        frame = pa_Ver_img
        Height, Width = frame.shape[:2]
        #print(Height, Width)

        img = cv2.resize(frame, (int(Width), int(Height)))
        cv2.rectangle(img, (300, 300), (Width - 200, Height - 200), (0, 0, 255), 10)

        dst = img[300:Height - 200, 300:Width - 200]
        PIL_Image = Image.fromarray(dst)
        

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        
        if k == 32:
            print("Capturing...")
            #text = pytesseract.image_to_string(PIL_Image, lang = 'eng')
            text = tool.image_to_string(PIL_Image, lang = 'eng', builder = pyocr.builders.TextBuilder())
            if (text != ""):
                    print('========================================================')
                    print(text)
                    print('========================================================')
                    with open(path + "\\text.txt", 'a', encoding='utf-8') as fObject:
                        fObject.write(text + '\n')
                    #f = open(path + '\\text.txt', 'a')
                    #f.write(text)


        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)#視窗可調整大小
        cv2.imshow('Camera', img)
        cv2.waitKey(100) 

cv2.destroyAllWindows()