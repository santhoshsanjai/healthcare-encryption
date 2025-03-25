from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('healthapp.urls')),  # Your app
    path('', include('django.contrib.auth.urls')),  # Login/Logout
]

