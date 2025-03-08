from django.urls import path, include
from . import views

urlpatterns = [    
    # [1] Users
    path('users-list/', views.users_list, name='users-list'),
    path('users-list/<int:pk>/', views.user_details, name='user-details'),
    
    # [2] Patients
    path('patients-list/', views.patients_list, name='patients-list'),
    path('patients-list/<int:user_id>/', views.patient_details, name='patient-details'),

    # [3] Doctors
    path('doctors-list/', views.doctors_list, name='doctors-list'),
    path('doctors-list/<int:user_id>/', views.doctor_details, name='doctor-details'),
    
    # [4] DoctorAvailability
    path('doctorav-list/', views.bookings_list, name='doctorav-list'),
    path('doctorav-list/<int:doctor_id>/', views.booking_details, name='doctorav-details'),
    
    # [5] Booking An Appointements
    path('book-appointments-list/', views.book_appointments_list, name='book_appointements_list'),
    path('book-appointments-list/<int:doctor_id>/', views.book_appointment_details, name='book_appointment-details'),
    path('book-appointments-list/<int:doctor_id>/<int:pk>/', views.book_appointment_details, name='book_appointment-details'),
        
    # Badr's Urls
    # [7] Login Api
    path("api/login/", views.custom_user_login, name="custom-user-login"),    
    
    # [8] PreviousHistory
    path('previous-history/',views.previous_history_api_view, name='previous-history'),
    path('previous-history/<int:sender_id>/',views.previous_history_api_view_details, name='previous-history-details'),
    path('previous-history/<int:sender_id>/<int:pk>/',views.previous_history_api_view_details, name='previous-history-details'),
    
    # [9] Photo Uploader
    path('photo-uploader/',views.upload_photo_api_view_list, name='photo_uploader'),  
    path('photo-uploader/<int:uploader_id>/',views.upload_photo_api_view_details, name='photo_uploader'),
    
    # [10] Alarm
    path('alarm/', views.alram_api_view_list, name='alarm-list'),  # List all alarms or create new (GET, POST) Methods
    path('alarm/<int:user_id>/', views.alarm_api_view_details, name='user-alarms'),  # Get all alarms for a specific user (GET)
    path('alarm/<int:user_id>/<int:pk>/', views.alarm_api_view_details, name='alarm-details'),  # Updating (PUT) or Deleteing (DELETE) specific alarm ! 
    
]
