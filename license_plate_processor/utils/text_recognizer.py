import cv2
import pytesseract
#import easyocr

config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789- '   #optimal configurations for pytesseract 

#reader = easyocr.Reader(['en']) 
def extract_easyocr(image):
    """Recognizes the characters on a preprocessed license plate image.
    
    Keyword arguments:
    image -- A file path or a numpy array representation of the image to be predicted.
    model_used -- A Model type to specify wether to use easyocr or pytesseract (defult=Model.EASY_OCR)
    exp_out_len -- The expected output length, excluding space and "-" characters. (defult=7)
    drop_excess -- Drop any characters recognized beyond exp_out_len. (defult=True)

    Return: return_description
    """
    output = ""
    output = reader.readtext(image, allowlist ='0123456789- ')  
    return output

def extract_pytesseract(image):
    config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789- '   #optimal configurations for pytesseract 
    #pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    return pytesseract.image_to_string(image, lang='eng', config=config).strip()