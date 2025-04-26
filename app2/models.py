from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models



class Room(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
        ('Normal', 'Normal'),
    ]
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default='available')
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)  # Add this field for room images

    def __str__(self):
        return f"{self.type} - ${self.price}"

class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField()
