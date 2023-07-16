from django.db import models

class LicensePlate(models.Model):
    id = models.AutoField(primary_key=True)
    plate_number = models.CharField(max_length=20)
    confidence_score = models.FloatField()
    image_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    device_identifier = models.CharField(max_length=50)
    device_location = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)


class ConnectedDevice(models.Model):
    id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    device_id = models.CharField(max_length=50)
    recording_time = models.DateTimeField()
    connection_time = models.DateTimeField(auto_now_add=True)
    device_location = models.CharField(max_length=100)