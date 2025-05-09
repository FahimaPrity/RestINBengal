from django import forms
from .models import Booking, Payment, Point
from django import forms
from .models import Booking, Payment, Point, Review

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

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['user', 'points_earned', 'points_used']

        # forms.py

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'rating', 'comment']

