from django.db import models

class LicensePlate(models.Model):
    plate_number = models.CharField(max_length=20)
    confidence_score = models.FloatField()
    image_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    device_identifier = models.CharField(max_length=50)
    device_location = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
