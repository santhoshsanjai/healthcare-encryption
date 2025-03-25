from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from healthapp import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin panel

    # Login and logout views
    path('', views.login_view, name='login'),  # Login page (default route)
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout, name='logout'),  # Logout view

    # Other app-specific views
    path('add/', views.add_record, name='add_record'),
    path('records/', views.view_records, name='records'),
    path('delete/<str:patient_id>/', views.delete_patient, name='delete_patient'),
    path('decrypt/<str:patient_id>/', views.decrypt_patient_data, name='decrypt_patient_data'),
]
handler404 = 'healthapp.views.custom_404_view'
