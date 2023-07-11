from .preprocessor import preprocess
from .yolo_model import predict
from PIL import Image
from .util_functions import formatt, encode_image_as_base64
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
    
    for car, plate in results:
        if(plate):
            x1, y1, x2, y2 = int(plate[0]), int(plate[1]), int(plate[2]), int(plate[3])
            plate = image[y1:y2, x1:x2]

            # Crop the license plate image to remove the flag (assuming it's on the right side)
            plate_cropped = plate[:, :plate.shape[1]]

            preprocessed_plate = preprocess(plate_cropped, height=50)
            text, confidence = ocr_reader.readtext(preprocessed_plate)
            print('#'*50)
            print(text)
            print('#'*50)
            if(confidence > 0.6):
                number = formatt(text)
                if(number):
                    encoded_image = encode_image_as_base64(Image.fromarray(plate_cropped))
                    detected = (number, confidence, encoded_image)
                    detections.append(detected)
    return detections 