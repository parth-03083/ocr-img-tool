from paddleocr import PaddleOCR,draw_ocr
import os

path = "C:\\Users\\workp\\workspace\\petpooja\\project\\picsum\\5.png"
ocr = PaddleOCR(use_angle_cls=True, lang='en')
result = ocr.ocr(path, rec=True, cls=False)

for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line[1][0])