from django.shortcuts import render, redirect
from license_plate_processor.views import process_file
from django.contrib import messages
from django.conf import settings
import os, time
from datetime import datetime
from license_plate_processor.models import LicensePlate
import json
from django.http import HttpResponse
from django.http import JsonResponse

import threading
from google.cloud import storage

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4'}


# Cloud functions
def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # The contents to upload to the file
    # The ID of your GCS object

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} uploaded to {bucket_name}."
    )


def download_blob_into_memory(bucket_name, blob_name):
    """Downloads a blob into memory."""
    # The ID of your GCS bucket
    # The ID of your GCS object

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    contents = blob.download_as_string()

    print(
        "Downloaded storage object {} from bucket {} as the following string: {}.".format(
            blob_name, bucket_name, contents
        )
    )





def index(request):
    # num_license_plates = 10  # Number of license plates to display
    # plates = LicensePlate.objects.order_by('-timestamp')[:num_license_plates]
    return render(request, 'car_tracker/index2.html') #, {'plates': plates}


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'No selected file')
            return redirect('index')
        if not allowed_extension(file.name):
            messages.error(request, 'Invalid file format')
            return redirect('index')

        recording_time_str = request.POST.get('recordingTime')
        if recording_time_str:
            recording_time = datetime.strptime(recording_time_str, '%Y-%m-%dT%H:%M')
        else:
            recording_time = None

        device_identifier = request.POST.get('deviceId')
        device_type = request.POST.get('deviceType')
        location = request.POST.get('deviceLocation')
        
        file_name, extension = file.name.split(".")
        file_path = os.path.join(settings.MEDIA_ROOT, file_name + "."+ extension)
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        print("$"*100)
        print("Finished Uploading File!")
        print("$"*100)
        data = None#file.read()
        #threading.Thread(target=upload_blob_from_memory, args=(settings.GS_BUCKET_NAME, data, device_identifier+"."+extension))
        results = process_file(data, extension, file_path, device_identifier, device_type, recording_time, location)
        # results's format = list of lists of dictionaries, each representing a license plate and its information.
        print(results)
        response_data = {
            'results': results
        }
        return HttpResponse(json.dumps(response_data, default=str), content_type='application/json')


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def search_by_time(request):
    if request.method == 'GET':
        time = request.POST.get('time')
        try:
            search_time = datetime.fromisoformat(time)
            plates = LicensePlate.objects.filter(timestamp__gte=search_time)
            return render(request, 'car_tracker/index.html', {'plates': plates})
        except ValueError:
            messages.error(request, 'Invalid time format')
    return redirect('index')

def search_by_plate(request):
    if request.method == 'GET':
        plate = request.GET.get('licensePlate')
        plates = LicensePlate.objects.filter(plate_number=plate)
        results = []
        for plate in plates:
            result = {
                'plate_number': plate.plate_number,
                'confidence_score': plate.confidence_score,
                'image_data': plate.image_data,
                'time': plate.timestamp,
                'device_identifier': plate.device_identifier,
                'device_type': plate.device_type,
                'location': plate.location,
            }
            results.append(result)
        return JsonResponse(results, safe=False)
    return redirect('index')



