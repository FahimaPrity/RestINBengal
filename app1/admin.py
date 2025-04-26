from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking, Payment, Point  # for app1
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Point)

