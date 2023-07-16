import base64
import io
import re
from collections import Counter
from datetime import timedelta, datetime

def format(number):
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
    """
    recording time format: "2023-07-15 13:17:06"
    # recording_time = 2023-07-15T14:10
    """
    print('recording_time inside calculate_frame_time should be 2023-07-15 14:33:54: ')
    print(recording_time)
    recording_datetime = datetime.strptime(recording_time, "%Y-%m-%d %H:%M:%S")
    frame_duration = timedelta(seconds=frame_count / fps)
    frame_time = recording_datetime - frame_duration
    return str(frame_time)

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

def format_plates_info(license_plates_info):
    license_plates = []
    for license_plate_id, plate_info in license_plates_info:
        plate_entry = {
            'license_plate_id': license_plate_id,
            **plate_info
        }
        license_plates.append(plate_entry)

    return license_plates

    
# def formatter(numbers):
#     format_1 = re.compile(r"^3-\d{4}-\d{2}$")
#     format_2 = re.compile(r"^\d-\d{4}-\d{2}$")
#     format_3 = re.compile(r"^3-\s?\d{4}-\s?\d{2}\s?$")
#     format_4 = re.compile(r"^\d-\s?\d{4}-\s?\d{2}\s?$")
#     format_5 = re.compile(r"^3-\d{4}-\d{2}.*$")
#     format_6 = re.compile(r"^\d{2}-\d{4}-\d{2}$")
#     format_7 = re.compile(r"^3-\s?(\d{4})-\s?(\d{2})\s?$")
#     format_8 = re.compile(r"^(\d{2})-\s?(\d{4})-\s?(\d{2})\s?$")
#     format_9 = re.compile(r"^3-\d{4}-\d{2}-$")
#     format_10 = re.compile(r"^3-\d{4}-\d{2}\s$")
#     format_11 = re.compile(r"^\d{2}-\s?\d{4}-\d{2}$")
#     format_12 = re.compile(r"^\d{2}-\s?\d{4}-\s?\d{2}$")
#     format_13 = re.compile(r"^\d{2}\s(\d{4})-(\d{2})$")


#     valid_numbers = []
#     exact_match = None
#     for number in numbers:
#         if format_1.match(number):
#             exact_match = number
#             valid_numbers.append(number)
#         elif format_2.match(number):
#             valid_numbers.append("3" + number[1:])
#         elif format_3.match(number):
#             match = format_1.search(number)
#             if match:
#                 valid_numbers.append(match.group())
#         elif format_4.match(number):
#             match = format_2.search(number)
#             if match:
#                 valid_numbers.append("3" + match.group()[1:])
#         elif format_5.match(number):
#             match = format_5.search(number)
#             if match:
#                 valid_numbers.append("3-" + match.group()[2:])
#         elif format_6.match(number):
#             match = format_6.search(number)
#             if match:
#                 valid_numbers.append("3-" + match.group())
#         elif format_7.match(number):
#             match = format_7.search(number)
#             if match:
#                 valid_numbers.append("3-" + match.group(1) + "-" + match.group(2))
#         elif format_8.match(number):
#             match = format_8.search(number)
#             if match:
#                 valid_numbers.append("3-" + match.group(2) + "-" + match.group(3))
#         elif format_9.match(number):
#             valid_numbers.append(number[:-1])
#         elif format_10.match(number):
#             valid_numbers.append(number.rstrip())
#         elif format_11.match(number):
#             match = format_11.search(number)
#             if match:
#                 valid_numbers.append(match.group().replace(" ", ""))
#         elif format_12.match(number):
#             match = format_12.search(number)
#             if match:
#                 valid_numbers.append(match.group().replace(" ", ""))
#         elif format_13.match(number):
#             match = format_13.search(number)
#             if match:
#                 valid_numbers.append("3-" + match.group(1) + "-" + match.group(2))

#     if exact_match:
#         return exact_match
#     elif len(valid_numbers) == 1:
#         return valid_numbers[0]
#     elif len(valid_numbers) > 1:
#         middle_parts = [number.split("-")[1] for number in valid_numbers]
#         counter = Counter(middle_parts)
#         most_common = counter.most_common(1)
#         if most_common:
#             final_number = "3-" + most_common[0][0] + "-**"
#             return final_number

#     return None