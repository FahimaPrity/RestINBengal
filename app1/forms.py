from django import forms
from .models import Booking, Payment, Point

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['user', 'points_earned', 'points_used']
