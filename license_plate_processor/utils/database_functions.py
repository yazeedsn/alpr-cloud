from license_plate_processor.models import LicensePlate


def save_license_plate_frame(frame):
    """
    Saves into the database the information from a list of license plates from a single frame.

    Parameters:
        frames (list): A list of license plate frames to be saved.

    Returns:
        None
    """
    license_plates = []

    for plate_info in frame:
        device_identifier = plate_info['device_identifier']
        device_type = plate_info['device_type']
        frame_time = plate_info['time']
        location = plate_info['location']
        valid_number = plate_info['plate_number']
        confidence_score = plate_info['confidence_score']
        encoded_image = plate_info['image_data']

        # Create a new LicensePlate instance
        license_plate = LicensePlate(
            plate_number=valid_number,
            confidence_score=confidence_score,
            image_data=encoded_image,
            timestamp=frame_time,
            device_identifier=device_identifier,
            device_type=device_type,
            location=location
        )
        license_plates.append(license_plate)

    # Save all the LicensePlate instances in the database
    LicensePlate.objects.bulk_create(license_plates)