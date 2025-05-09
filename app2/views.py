from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect

from app1.forms import BookingForm
from app1.models import Booking
from app2.models import Room, Review
from app2.forms import ReviewForm
def view_rooms(request):
    rooms = Room.objects.all()  # Fetch all rooms
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'room.html', {'rooms': rooms, 'bookings': bookings})
def leave_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()  # Save the review to the database
            return redirect('home')  # Redirect to the home page after saving the review
    else:
        form = ReviewForm()
    reviews = Review.objects.all()  # Fetch all reviews
    return render(request, 'review.html', {'form': form, 'reviews': reviews})  # Pass reviews to template




