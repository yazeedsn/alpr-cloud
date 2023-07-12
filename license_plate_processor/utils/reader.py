from .preprocessor import preprocess
from .yolo_model import predict
from PIL import Image
from .util_functions import formatt, encode_image_as_base64
from math import floor, ceil
import cv2


def read_image(image, ocr_reader):
    """
    takes an image and returns the license plates inside this image as well as their information
    and stores the results in the database

    Parameters:
        image, ocr_reader, device_identifier, device_type, frame_time, location

    Returns:
        list: A list of tuple, each containing a plate number, it's confidence score, it's base64 encoded image respectivly.
            Each tuple has the following format:
                (plate_number, confidence_score, encoded_image)
    """

    if isinstance(image, str):
        image = cv2.imread(image)

    results = predict(image)  # xy coordinates of all license plates
    detections = []
    _, x_orig, _ = image.shape

    for car, plate in results:
        x1, y1, x2, y2 = ceil(plate[0]), ceil(plate[1]), floor(plate[2]), floor(plate[3])
        # add some padding, improves some of the results
        if not ((x1 < 10) or (x2 > x_orig-10)):
            x1 -= 10
            x2 += 10
        plate = image[y1:y2, x1:x2]
        preprocessed_plate = preprocess(plate, height=50)
        text, confidence = ocr_reader.readtext(preprocessed_plate)
        if(confidence > 0.6):
            number = formatt(text)
            if(number):
                encoded_image = encode_image_as_base64(Image.fromarray(plate))
                detected = (number, confidence, encoded_image)
                detections.append(detected)
    return detections 