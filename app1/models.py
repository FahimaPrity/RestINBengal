from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from app2.models import Room

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.id}"

class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points_earned = models.IntegerField(default=0)
    points_used = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Earned: {self.points_earned}, Used: {self.points_used}"
