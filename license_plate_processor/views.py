from .utils.reader import read_image
from .utils.database_functions import save_frame_data
import cv2
import time
from .utils.util_functions import calculate_frame_time
from datetime import datetime
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from .utils.ocr_reader import PaddleOCR
from .utils.util_functions import format_plates_info


def process_video(ocr_reader, file_path, device_info, shared_data, shared_data_lock):
    device_identifier = device_info['device_id']
    device_type = device_info['device_type']
    recording_time = device_info['recording_time'] # recording_time = 2023-07-15T14:10
    location = device_info['location']

    cap = cv2.VideoCapture(file_path)
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    with shared_data_lock:
        shared_data[device_identifier] = {
            'results': [],
            'finished_processing': False
        }

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f'Finished processing the video for device: {device_identifier}')
            break

        frame_count += 1
        frame_time = calculate_frame_time(frame_count, fps, recording_time)

        # 2023-07-15 14:33:54
        extracted_frame_data = read_image(frame, ocr_reader, device_identifier, device_type, frame_time, location)
        license_plates_info = save_frame_data(extracted_frame_data)
        format_plates_info(license_plates_info)

        with shared_data_lock:
            if device_identifier in shared_data:
                shared_data[device_identifier]['results'].append(extracted_frame_data)

    cap.release()

    with shared_data_lock:
        shared_data[device_identifier]['finished_processing'] = True
