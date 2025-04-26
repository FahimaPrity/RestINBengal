from django.urls import path
from . import views

urlpatterns = [
     # Homepage view
    path('rooms/', views.view_rooms, name='view_rooms'),
    path('review/', views.leave_review, name='leave_review'),
]
