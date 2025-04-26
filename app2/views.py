from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect

from app1.forms import BookingForm
from app2.models import Room, Review
from app2.forms import ReviewForm
def view_rooms(request):
    rooms = Room.objects.all()  # Fetch all rooms
    return render(request, 'room.html', {'rooms': rooms})
def leave_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()  # Save the review to the database
            return redirect('home')  # Redirect to the home page after saving the review
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form})



