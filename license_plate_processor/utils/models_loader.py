from .ocr_reader import PaddleOCR

from ultralytics import YOLO
import torch
import os

# Settings for the models
_weights_path = os.path.join(os.path.dirname(__file__), "yolo_weights/best.pt")
_device = 'cuda' if torch.cuda.is_available() else 'cpu'
_use_gpu_paddle_ocr = True if torch.cuda.is_available() else False

#Loading models
yolo_model = YOLO(_weights_path)
yolo_model.to(_device)

intilized_ocr = PaddleOCR(use_gpu=_use_gpu_paddle_ocr)
