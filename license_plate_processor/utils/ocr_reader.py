from abc import ABC, abstractmethod
from paddleocr import PaddleOCR as POCR

import pytesseract
import easyocr


#Abstract OCR class, consistent interface.
class OCR_Reader(ABC):

    @abstractmethod
    def readtext(self, image):
        pass


class EasyOCR(OCR_Reader):
    
    def __init__(self, allowed_list='0123456789- '):
        self._reader = easyocr.Reader(['en'])
        self._allowed_list = allowed_list

    def readtext(self, image):
        text = self._reader.readtext(image, detail=0, paragraph=False, allowlist =self._allowed_list)
        return text

class PytesseractOCR(OCR_Reader):
    
    def __init__(self, allowed_list='0123456789- ', psm=6, oem=3):
        self._config = f'--psm {psm} --oem {oem} -c tessedit_char_whitelist={allowed_list}'
        

    def readtext(self, image):
        text = pytesseract.image_to_string(image, lang='eng', config=self._config).strip()
        if(text):
            return text
        else:
            return ''

class PaddleOCR(OCR_Reader):
    def __init__(self, use_gpu=True):
        self._reader = POCR(use_angle_cls=True, lang='en', use_gpu=use_gpu)
    
    def readtext(self, image):
        results = self._reader.ocr(image, det=False, cls=True)
        if(results):
            print("ocr_reader -> readtext -> results:")
            print(results)
            if(results[0]):
                return results[0][0]
        return ''
