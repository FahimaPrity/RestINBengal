from django import forms
from .models import Room, Review

# Room Form (if needed for another purpose)
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['type', 'price', 'status']

# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['room', 'reviewer_name', 'comment', 'rating']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['room'].label_from_instance = lambda obj: f"{obj.type} - ${obj.price}"  # Displaying room details
