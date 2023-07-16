from license_plate_processor.models import LicensePlate, ConnectedDevice
from datetime import datetime, timedelta


def save_frame_data(frame):
    """
    Saves into the database the information from a list of license plates from a single frame.

    Parameters:
        frames (list): A list of license plate frames to be saved.

    Returns:
        None
    """
    license_plate_info = []

    for plate_info in frame:
        device_identifier = plate_info['device_identifier']
        device_type = plate_info['device_type']
        frame_time = plate_info['time']
        location = plate_info['location']
        valid_number = plate_info['plate_number']
        confidence_score = plate_info['confidence_score']
        encoded_image = plate_info['image_data']

        if '.' in frame_time:
            frame_time_without_ms = frame_time.split('.')[0]  # Remove the milliseconds
        else:
            frame_time_without_ms = frame_time

        frame_time_object = datetime.strptime(frame_time_without_ms, '%Y-%m-%d %H:%M:%S')
        last_minute = frame_time_object - timedelta(minutes=1)
        last_minute_str = last_minute.strftime('%Y-%m-%d %H:%M:%S')

        duplicate_exists = LicensePlate.objects.filter(
            plate_number=valid_number,
            device_identifier=device_identifier,
            timestamp__gte=last_minute_str,
            timestamp__lte=frame_time_without_ms
        ).exists()

        if duplicate_exists:
            continue

        license_plate = LicensePlate(
            plate_number=valid_number,
            confidence_score=confidence_score,
            image_data=encoded_image,
            timestamp=frame_time_without_ms,  # Save without milliseconds
            device_identifier=device_identifier,
            device_type=device_type,
            location=location,
        )

        license_plate.save()
        license_plate_info.append((license_plate.id, plate_info))

    return license_plate_info


def store_new_device(device_info):
    connected_device = ConnectedDevice(
            device_name=device_info['device_name'],
            device_type=device_info['device_type'],
            device_id=device_info['device_id'],
            recording_time=device_info['recording_time'],
            device_location=device_info['location']
        )
        
    connected_device.save()
    return