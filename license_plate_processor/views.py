from .utils.reader import read_image
from .utils.models_loader import intilized_ocr
from .utils.database_functions import save_license_plate_frame
from .utils.util_functions import calculate_frame_time, encapsulate_record

from io import BytesIO
import threading
import cv2
import time
import numpy as np


def process_file(file, extension, device_identifier, device_type, recording_time, location):
    """
    takes a file (image, video, IP for a camera), verifies it, then extracts license plate information from each frame from that file

    Parameters:
        file_path, device_identifier, device_type, recording_time, location

    Returns:
        list of lists: each sublist contains dictionaries, each dictionary representing a license plate and its information from a specific frame.
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
        ex: [[(), ()], [()], [(), (), ()]]
    """

    image_extension = ['jpg', 'png', 'jpeg']
    video_extension = ['mp4']
    isImage = False
    all_results = []

    if extension in image_extension:
        isImage = True
    elif extension not in video_extension:
        exit('file extension is not recognized, please upload a video or an image')

    results = []

    if isImage:
        data = BytesIO()
        for chunk in file.chunks():
            data.write(chunk)
        data.seek(0)
        nparr = np.frombuffer(data.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        detections = read_image(image, intilized_ocr)
        records = _get_records(detections, device_identifier, device_type, recording_time, location)
        save_license_plate_frame(records)
        results.append(records)

    else:
        if file.content_type.startswith('video'):
            cap = cv2.VideoCapture(file.temporary_file_path())
            frame_count = 0
            second_count = 0
            fps = cap.get(cv2.CAP_PROP_FPS)
            reading_thread = None
            result = [None]
            start_time = time.time()
            while True:
                ret, frame = cap.read()

                if not ret:
                    # No more frames in the video
                    print('Finished processing the video')
                    break
                if(frame_count == fps):
                    frame_count = 0
                    second_count += 1
                frame_count += 1
                frame_time = calculate_frame_time(frame_count, fps, recording_time)
                if not reading_thread or not reading_thread.is_alive():
                    if(result[0] != None):
                        records = _get_records(result[0], device_identifier, device_type, recording_time, location)
                        save_license_plate_frame(records)
                        results.append(records)
                    reading_thread = threading.Thread(target=read, args=(frame, intilized_ocr, result))
                    reading_thread.start()
                time.sleep(1/fps)
            
    
            end_time = time.time()
            print(f"Run Time: {end_time - start_time: .2f}")
            cap.release()
    return results

def read(frame, ocr_reader, result):
    detections = read_image(frame, ocr_reader)
    result[0] = detections

def matching_digits(number1, number2):
    assert len(number1) == len(number2)
    matches = 0
    for i in range(len(number1)):
        if(number1[i] == number2[i]):
            matches += 1
    return matches

def _get_records(detections, device_identifier, device_type, recording_time, location):
    records = []

    for detection in detections:
        plate_number, confidence_score, encoded_image = detection
        record = encapsulate_record(plate_number, confidence_score, encoded_image, time, device_identifier, device_type, location)
        records.append(record)
    
    return records