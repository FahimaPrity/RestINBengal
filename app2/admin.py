from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Review  # Import Room and Review models

admin.site.register(Room)
admin.site.register(Review)

