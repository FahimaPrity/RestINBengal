from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from app1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('book/', views.book_room, name='book_room'),
    path('payment/<int:booking_id>/', views.make_payment, name='make_payment'),
    path('points/', views.view_points, name='view_points'),
    path('create-point/', views.create_point, name='create_point'),
]
