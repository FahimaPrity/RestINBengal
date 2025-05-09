from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import timedelta

from .models import Booking, Payment, Point
from app2.models import Room, Review
from .forms import BookingForm, PaymentForm, PointForm, ReviewForm


# ✅ Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# ✅ Home view
@login_required(login_url='login')
def home(request):
    total_points = 0
    point_obj = Point.objects.filter(user=request.user).first()
    if point_obj:
        total_points = point_obj.points_earned

    bookings = Booking.objects.filter(user=request.user)
    payments = Payment.objects.filter(booking__user=request.user)
    rooms = Room.objects.all()
    reviews = Review.objects.all()

    return render(request, 'home.html', {
        'bookings': bookings,
        'payments': payments,
        'rooms': rooms,
        'reviews': reviews,
        'total_points': total_points,
    })


# ✅ Admin dashboard


# ✅ Book room view
@login_required(login_url='login')
def book_room(request):
    if request.user.is_superuser:
        return HttpResponseForbidden("Admins cannot book rooms.")

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            if room.status == 'available':
                room.status = 'not available'
                room.save()

                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()

                # Add 10 points
                point_obj, created = Point.objects.get_or_create(user=request.user)
                point_obj.points_earned = F('points_earned') + 10
                point_obj.save()
                point_obj.refresh_from_db()

                return redirect('make_payment', booking_id=booking.id)
            else:
                form.add_error('room', 'This room is already booked or unavailable.')
    else:
        form = BookingForm()

    rooms = Room.objects.filter(status='available')
    return render(request, 'book_room.html', {'form': form, 'rooms': rooms})


# ✅ Make payment view
@login_required(login_url='login')
def make_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    nights = (booking.check_out - booking.check_in).days
    total_amount = booking.room.price * nights

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount != total_amount:
                messages.error(request, f"❌ You must pay exactly {total_amount} ৳.")
            else:
                payment = form.save(commit=False)
                payment.booking = booking
                payment.user = request.user
                payment.save()

                messages.success(request, "✅ Payment here")

                # Add 10 points for payment (optional)
                point_obj, created = Point.objects.get_or_create(user=request.user)
                point_obj.points_earned = F('points_earned') + 10
                point_obj.save()
                point_obj.refresh_from_db()

                return redirect('view_points')
    else:
        form = PaymentForm(initial={'amount': total_amount})

    return render(request, 'payment.html', {
        'form': form,
        'booking': booking,
        'nights': nights,
        'total_amount': total_amount,
    })


# ✅ View points
@login_required(login_url='login')
def view_points(request):
    point_obj, created = Point.objects.get_or_create(user=request.user)
    total_points = point_obj.points_earned
    return render(request, 'points.html', {'total_points': total_points})


# ✅ About view
def about_view(request):
    return render(request, 'about.html')


# ✅ Create point (optional)
def create_point(request):
    if request.method == 'POST':
        form = PointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_points')
    else:
        form = PointForm()
    return render(request, 'points.html', {'form': form})


# ✅ Leave review
@login_required(login_url='login')
def leave_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('leave_review')
    else:
        form = ReviewForm()

    reviews = Review.objects.all()
    return render(request, 'review.html', {'form': form, 'reviews': reviews})


# ✅ Cancel booking
@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    room = booking.room
    booking.delete()
    room.status = 'available'
    room.save()
    # 3️⃣ Points কমাও
    point_obj, created = Point.objects.get_or_create(user=request.user)
    if point_obj.points_earned >= 10:
        point_obj.points_earned = F('points_earned') - 20
        point_obj.save()
        point_obj.refresh_from_db()
    else:
        # যদি points 0 এর নিচে চলে যায়, তাহলে 0 রাখো
        point_obj.points_earned = 0
        point_obj.save()


    return redirect('view_rooms')
