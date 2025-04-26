from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),  # Handles home, book, payment, points
    path('', include('app2.urls')),  # Handles rooms, reviews
  ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
