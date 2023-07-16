# Generated by Django 4.2.2 on 2023-07-14 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_plate_processor', '0002_connecteddevice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='licenseplate',
            name='vehicle_type',
        ),
        migrations.AddField(
            model_name='licenseplate',
            name='car_color',
            field=models.CharField(default='unknown', max_length=50),
            preserve_default=False,
        ),
    ]