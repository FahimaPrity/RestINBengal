from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from app2.models import Room
from django.db import models
from django.contrib.auth.models import User

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

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField()  # 1 থেকে 5 পর্যন্ত রেটিং
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer_name} - Rating: {self.rating}"