from datetime import timedelta, datetime

import base64
import io
import re

def encapsulate_record(number, confidence, encoded_image, time, device_id, device_type, location):
    record = {
        'plate_number': number,
        'confidence_score': confidence,
        'image_data': encoded_image,
        'time': time,
        'device_identifier': device_id,
        'device_type': device_type,
        'location': location,
    }

    return record

def formatt(number):
    non_digit_pattern = re.compile('[^\d]+')
    start_3_pattern = re.compile('3.{6}')

    digits = non_digit_pattern.sub('', number)
    correct_number = start_3_pattern.findall(digits)
    if(correct_number):
        final_format = re.sub(r'(\d)(\d{4})(\d{2})', r'\1-\2-\3', correct_number[0])
        return final_format
    else:
        if(len(digits) == 6 and digits[0] != '3'):
            digits = '3' + digits
            final_format = re.sub(r'(\d)(\d{4})(\d{2})', r'\1-\2-\3', digits)
            return final_format
    
def encode_image_as_base64(image):
    with io.BytesIO() as output:
        image.save(output, format='JPEG')
        plate_bytes = output.getvalue()
        encoded_image = base64.b64encode(plate_bytes).decode('utf-8')
    return encoded_image


def calculate_frame_time(frame_count, fps, recording_time):
    frame_time =  timedelta(seconds=frame_count / fps) #recording_time +
    return frame_time