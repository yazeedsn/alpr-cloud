from django.contrib import admin
from django.urls import path, include
from car_tracker import views
from license_plate_processor import views as processor_views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_by_plate/', views.search_by_plate, name='search_by_plate'),
    path('upload/', views.handle_new_device, name='handle_new_device'),
    path('update_license_plate/', views.update_license_plate, name='update_license_plate'),
    path('remove_device/', views.remove_device, name='remove_device'),
    path('device-data/<str:device_id>/', views.get_device_data, name='get_device_data'),
]



