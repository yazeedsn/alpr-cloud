from .ocr_reader import PaddleOCR
#from .color_recognition import color_histogram_feature_extraction

from ultralytics import YOLO
import torch
import os

print("#"*50 + "Intilizing Models" + "#"*50)
print("Intlilizng YOLO:")
# Settings for the models
_weights_path = os.path.join(os.path.dirname(__file__), "yolo_weights", "best.pt")
_device = 'cuda' if torch.cuda.is_available() else 'cpu'
_use_gpu_paddle_ocr = False#True if torch.cuda.is_available() else False

#Loading yolo model
yolo_model = YOLO(_weights_path)
yolo_model.to(_device)

print("\nIntlilizng OCR:")
#Intilizing and loading paddel ocr reader
intilized_ocr = PaddleOCR(use_gpu=_use_gpu_paddle_ocr)
print("\n"+"#"*115 + "\n")

# Loading colors model
# PATH = os.path.join(os.path.dirname(__file__), 'color_recognition', 'colors_data','training.data')

# if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
#     print ('training data is ready, classifier is loading...')
# else:
#     print ('training data is being created...')
#     open(PATH, 'w')
#     color_histogram_feature_extraction.training()
#     print ('training data is ready, classifier is loading...')