from .preprocessor import preprocess
from .yolo_model import predict
from PIL import Image
from .util_functions import format, encode_image_as_base64
import cv2
from .color_detector import get_image_color
import os


def read_image(image, ocr_reader, device_identifier, device_type, frame_time, location):
    """
    takes an image and returns the license plates inside this image as well as their information
    and stores the results in the database

    Parameters:
        image, ocr_reader, device_identifier, device_type, frame_time, location

    Returns:
        list: A list of dictionaries, each representing a license plate and its information.
            Each dictionary has the following format:
                {
                    'plate_number': valid_number,
                    'confidence_score': confidence_score,
                    'image_data': encoded_image,
                    'time': frame_time,
                    'device_identifier': device_identifier,
                    'device_type': device_type,
                    'location': location,
                }
    """

    if isinstance(image, str):
        image = cv2.imread(image)

    results = predict(image)  
    frames = []
    _, x_orig, _ = image.shape
    i = 0
    for car, plate in results:
        print("prediction....")
        x1_p, y1_p, x2_p, y2_p = int(plate[0]), int(plate[1]), int(plate[2]), int(plate[3])
        if not ((x1_p < 10) or (x2_p > x_orig-10)):
            x1_p -= 10
            x2_p += 10
        plate_cropped = image[y1_p:y2_p, x1_p:x2_p]

        if(car):
            x1_car, y1_car, x2_car, y2_car = int(car[0]), int(car[1]), int(car[2]), int(car[3])
            car_image = image[y1_car:y2_car, x1_car:x2_car]
            
            # car_color = get_image_color(car_image) # check this
            #output_dir = 'temp'
            #os.makedirs(output_dir, exist_ok=True)
            #output_filename = 'car_' + str(i) + '.jpg'
            #output_path = os.path.join(output_dir, output_filename)
            #cv2.imwrite(output_path, image)


        preprocessed_plate = preprocess(plate_cropped, height=50)
        text, confidence = ocr_reader.readtext(preprocessed_plate)
        print(text, confidence)
        if(confidence > 0.6):
            valid_number = format(text)
            if(valid_number):
                encoded_image = encode_image_as_base64(Image.fromarray(plate_cropped))

                frame_info = {
                    'plate_number': valid_number,
                    'confidence_score': confidence,
                    'image_data': encoded_image,
                    'time': frame_time,
                    'device_identifier': device_identifier,
                    'device_type': device_type,
                    'location': location,
                }
                    
                frames.append(frame_info)
                print(valid_number)

    return frames


