from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime, timezone
from license_plate_processor.views import process_video
from license_plate_processor.models import LicensePlate, ConnectedDevice
from license_plate_processor.utils.database_functions import store_new_device, save_frame_data
from license_plate_processor.utils.util_functions import format_plates_info
from license_plate_processor.utils.models_loader import intilized_ocr
from license_plate_processor.views import read_image
import json, os, threading



ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4'}
ocr_reader = intilized_ocr
def initialize_ocr_reader():
    global ocr_reader
    if ocr_reader is None:
        ocr_reader = PaddleOCR()

initialize_ocr_reader()




def index(request):
    connected_devices = ConnectedDevice.objects.all()
    license_plates = LicensePlate.objects.all()
    license_plates_data = []
    for plate in license_plates:
        plate_data = {
            'license_plate_id': plate.id,
            'plate_number': plate.plate_number,
            'confidence_score': plate.confidence_score,
            'image_data': plate.image_data,
            'time': plate.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 
            'device_identifier': plate.device_identifier,
            'device_location': plate.device_location,
            'location': plate.location,
        }
        license_plates_data.append(plate_data)

    return render(request, 'car_tracker/index2.html', {
        'connected_devices': connected_devices,
        'license_plates': json.dumps(license_plates_data),
    })


shared_data = {}
shared_data_lock = threading.Lock()

def handle_new_device(request):
    global ocr_reader
    confirm_request_is_post(request)

    device_info = get_device_info(request)
    store_new_device(device_info)

    check_file_integrity(request)
    file_path = load_file_to_server(request)


    if device_info['device_type'] == 'image':
        extracted_frame_data = read_image(file_path, ocr_reader, \
            device_info['device_id'], \
            device_info['device_type'], \
            device_info['recording_time'],  \
            device_info['location'])

        print(device_info['recording_time']) # 2023-07-15 14:33:54

        license_plates_info = save_frame_data(extracted_frame_data)
        results = format_plates_info(license_plates_info)


    elif device_info['device_type'] == 'video':
        threading.Thread(target=process_video, args=(ocr_reader, file_path, device_info, shared_data, shared_data_lock)).start()
        results = []

    response_data = {
        'success': True,
        'results': results,
        'startedProcessing': device_info['device_type'] == 'video'
    }
    return HttpResponse(json.dumps(response_data, default=str), content_type='application/json')


def get_device_info(request):
    device_name = request.POST.get('deviceName')
    device_type = request.POST.get('deviceType')
    device_id = request.POST.get('deviceId')
    recording_time=request.POST.get('recording_time')
    location = request.POST.get('deviceLocation')

    if not recording_time:
        recording_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    device_info = {
        'device_name': device_name,
        'device_id': device_id,
        'device_type': device_type,
        'location': location,
        'recording_time': recording_time
    }

    return device_info


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def search_by_plate(request):
    if request.method == 'GET':
        plate = request.GET.get('licensePlate')
        start_time = request.GET.get('startTime')
        end_time = request.GET.get('endTime')

        # Prepare the query filter
        query_filter = Q(plate_number=plate)

        # Check if start time is specified
        if start_time:
            start_time = make_aware(datetime.strptime(start_time, "%Y-%m-%dT%H:%M"), timezone.utc)
            query_filter &= Q(timestamp__gte=start_time)

        # Check if end time is specified
        if end_time:
            end_time = make_aware(datetime.strptime(end_time, "%Y-%m-%dT%H:%M"), timezone.utc)
            query_filter &= Q(timestamp__lte=end_time)

        # Query the database with the filter
        plates = LicensePlate.objects.filter(query_filter)

        results = []
        for plate in plates:
            result = {
                'license_plate_id': plate.id,
                'plate_number': plate.plate_number,
                'confidence_score': plate.confidence_score,
                'image_data': plate.image_data,
                'start_time': start_time.strftime("%Y-%m-%d %H:%M") if start_time else '',
                'end_time': end_time.strftime("%Y-%m-%d %H:%M") if end_time else '',
                'time': plate.timestamp,
                'device_identifier': plate.device_identifier,
                'device_type': plate.device_type,
                'location': plate.location,
            }
            results.append(result)

        return JsonResponse(results, safe=False)

    return redirect('index')


def update_license_plate(request):
    if request.method == 'POST':
        license_plate_id = request.POST.get('id')
        new_plate_number = request.POST.get('plate_number')

        try:
            license_plate = LicensePlate.objects.get(id=license_plate_id)
            license_plate.plate_number = new_plate_number
            license_plate.save()
            return JsonResponse({'success': True})
        except LicensePlate.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'License plate not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def remove_device(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        device_id = payload.get('device_id')
        print(device_id)
        print('removing device..')
        ConnectedDevice.objects.filter(device_id=device_id).delete()
        print('device removed.')

        response_data = {
            'success': True,
            'message': 'Device removed successfully',
        }
        return JsonResponse(response_data)


def confirm_request_is_post(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def check_file_integrity(request):
    file = request.FILES.get('file')

    if not file:
        messages.error(request, 'No selected file')
        return redirect('index')
    if not allowed_extension(file.name):
        messages.error(request, 'Invalid file format')
        return redirect('index')


def load_file_to_server(request):
    file = request.FILES.get('file')

    filename = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path
        

def get_device_data(request, device_id):
    response_data = {}
    with shared_data_lock:
        if device_id in shared_data:
            device_data = shared_data[device_id]
            response_data['results'] = device_data['results']
            response_data['finishedProcessing'] = device_data['finished_processing']
            if device_data['finished_processing']:
                del shared_data[device_id]
        else:
            # Device ID not found, assume finished processing
            response_data['results'] = []
            response_data['finishedProcessing'] = True

    return JsonResponse(response_data)

