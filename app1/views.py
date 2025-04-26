from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import F
from django.contrib.auth.models import User
from .models import Booking, Payment, Point
from app2.models import Room, Review
from .forms import BookingForm, PaymentForm, PointForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login


# Register view for user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('home')  # Redirect to home page after login
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# Home view that shows user bookings, payments, and points
@login_required(login_url='login')
def home(request):
    total_points = 0
    try:
        # Calculate total points earned by the user
        total_points = Point.objects.filter(user=request.user).first().points_earned if Point.objects.filter(
            user=request.user).exists() else 0
    except:
        pass

    # Filter objects based on the current logged-in user
    bookings = Booking.objects.filter(user=request.user)
    payments = Payment.objects.filter(booking__user=request.user)
    points = Point.objects.filter(user=request.user)
    rooms = Room.objects.all()
    reviews = Review.objects.all()

    return render(request, 'home.html', {
        'bookings': bookings,
        'payments': payments,
        'points': points,
        'rooms': rooms,
        'reviews': reviews,
        'total_points': total_points,  # Show total points on home page
    })


# Booking view for booking a room
@login_required(login_url='login')
def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            # Check if room is available
            if room.status == 'available':
                # Book the room and mark it as not available
                room.status = 'not available'
                room.save()

                booking = form.save(commit=False)
                booking.user = request.user  # Assuming the user is logged in
                booking.save()

                # Award 10 points to the user upon booking
                user = request.user
                point_obj, created = Point.objects.get_or_create(user=user)
                point_obj.points_earned = F('points_earned') + 10
                point_obj.save()
                point_obj.refresh_from_db()

                # Redirect to payment page
                return redirect('make_payment', booking_id=booking.id)
            else:
                form.add_error('room', 'This room is already booked or unavailable.')
    else:
        form = BookingForm()

    rooms = Room.objects.filter(status='available')
    return render(request, 'book_room.html', {'form': form, 'rooms': rooms})


# Payment view for making a payment for a booking
@login_required(login_url='login')
def make_payment(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist")

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()

            # Award 10 points to the user for payment
            user = booking.user
            point_obj, created = Point.objects.get_or_create(user=user)
            point_obj.points_earned = F('points_earned') + 10
            point_obj.save()
            point_obj.refresh_from_db()

            return redirect('view_points')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'booking': booking})


# View to display the points the user has earned
@login_required(login_url='login')
def view_points(request):
    # Get the points object for the user (if any)
    point_obj, created = Point.objects.get_or_create(user=request.user)

    # Calculate the total points by summing the points earned for each booking
    total_points = sum(10 for booking in Booking.objects.filter(user=request.user))

    point_obj.points_earned = total_points  # Update the points earned for the user
    point_obj.save()

    # Display the total points on the points page
    return render(request, 'points.html', {'total_points': total_points})


# Create points form for manual creation of points (optional)
def create_point(request):
    if request.method == 'POST':
        form = PointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_points')
    else:
        form = PointForm()

    return render(request, 'points.html', {'form': form})
