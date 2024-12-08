# File: admin.py
# Author: Jared Chou (jchou@bu.edu) 2024
# Description: Register the different models to the django Admin so they can be viewed through the 
# django admin tool

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Trip)
admin.site.register(Profile)
admin.site.register(Cost)
admin.site.register(Image)
admin.site.register(AttendTrip)
