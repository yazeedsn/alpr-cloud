# Generated by Django 4.2.2 on 2023-07-06 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LicensePlate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('plate_number', models.CharField(max_length=20)),
                ('confidence_score', models.FloatField()),
                ('image_data', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('device_identifier', models.CharField(max_length=50)),
                ('device_location', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(max_length=20)),
            ],
        ),
    ]
