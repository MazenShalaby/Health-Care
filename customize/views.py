from .models import User, Profile, DoctorsProfileInfo, Booking_Appointments, DoctorAvailability, PreviousHistory, UploadedPhoto, Alarm
from .serializers import  (UserSerializer, ProfileSerializer, DoctorInfoSerializer, AppointmentSerializer, DoctorAvailabilitySerializer,
CustomUserLoginSerializer , PreviousHistorySerializer, UploadedPhotoSerializer, AlarmSerializer)

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

########################################################################## {Django REST Framework} #########################################################################################################

################################################################################# [1] Users ###############################################################################################################################################################################################################################################

# [1.1] ==> User(s) List
@api_view(['GET', 'POST'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def users_list(request):
    
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Password will be hashed by the serializer
            retrieved_user = User.objects.get(pk=user.pk)  # Fetch full instance for response
            retrieved_serializer = UserSerializer(retrieved_user)
            return Response(retrieved_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# [1.2] ==> Specific User Details
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def user_details(request, pk):
    
    try:
        # Fetch the profile based on the user_id
        profile = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(profile, many=False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        profile.delete()
        return Response({"message": "User deleted successfully"})
    
############################################################## [2] Patients ##############################################################

# [2.1] ==> Patient(s) List
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def patients_list(request):
    
    if request.method == "GET":
        users = Profile.objects.all()
        serializers = ProfileSerializer(users, many=True)
        return Response(serializers.data)
    
    elif request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# [2.1] ==> Specific User Details 
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def patient_details(request, user_id):
    
    try:
        # Fetch the profile based on the user_id
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the profile information
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the profile
        profile.delete()
        return Response({"message": "Profile deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

############################################################## [3] Doctors ##############################################################

# [3.1] ==> Doctor(s) List 
@api_view(['GET'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def doctors_list(request):
    
    if request.method == 'GET':
        doctors = DoctorsProfileInfo.objects.all()
        serializer = DoctorInfoSerializer(doctors, many=True)
        return Response(serializer.data)
    
# [3.1] ==>  Specific Doctor Details 
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def doctor_details(request, user_id):
    
    try:
        # Fetch the doctor profile based on the user_id
        doctor = DoctorsProfileInfo.objects.get(user_id=user_id)
    except DoctorsProfileInfo.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Serialize and return the doctor's information
        serializer = DoctorInfoSerializer(doctor, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the doctor's information
        serializer = DoctorInfoSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # Delete the doctor's profile
        doctor.delete()
        return Response({"message": "Doctor profile deleted successfully!"})
    
############################################################## [4] Doctor Availability ##############################################################

# [4.1] ==>  Doctor Availability(s) List
@api_view(['GET', 'POST', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def bookings_list(request):
    
    appointment = DoctorAvailability.objects.all()
    if request.method == 'GET':
        serializer = DoctorAvailabilitySerializer(appointment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DoctorAvailabilitySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Booking has been added successfully :) "}, status= status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        appointment.delete()
        return Response({"message": "All Bookings(s) deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"message": "Can't add same data entry :( "}, status=status.HTTP_400_BAD_REQUEST)
    
# [4.2] ==>  Specific Doctor Availability Details 
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def booking_details(request, doctor_id):
    
    try:
        # Fetch all Activity Feeds associated with the given doctor
        booking = DoctorAvailability.objects.filter(doctor_id=doctor_id)
        if not booking.exists():
            return Response({"error": "No Booking found for the given doctor ID"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid doctor ID"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Retrieve all Activity Feeds for the doctor
        serializer = DoctorAvailabilitySerializer(booking, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        return Response(
            {"error": "Cannot update multiple Bookings(s) at once. Update a specific Booking by its ID."},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        # Delete all Activity Feeds for the doctor
        deleted_count, _ = booking.delete()
        return Response({"message": f"{deleted_count} Bookings(s) deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

############################################################## [5] Booking An Appointments ##############################################################

# [5.1] ==>  Appointment(s) List
@api_view(['GET', 'POST', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def book_appointments_list(request):
    """
    - GET : Retrieve all appointments.
    - POST : Create a new appointment, ensuring no duplicate bookings for the same doctor, date, and time.
    - DELETE : Delete all appointments.
    - You can fetch all appointments associated with doctor via (book-appointments-list/doctor_id/)
    """
    if request.method == 'GET':
        appointments = Booking_Appointments.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data['doctor']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']

            # Check if the appointment slot is already booked by another patient
            if Booking_Appointments.objects.filter(doctor=doctor, date=date, time=time, available=False).exists():
                return Response(
                    {"error": "This appointment slot is already booked by another patient."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the new appointment
            appointment = serializer.save()

            # Ensure the appointment is marked as unavailable
            appointment.available = False
            appointment.save(update_fields=['available'])

            return Response(
                {"message": "An appointment has been booked successfully!", "data": serializer.data}, 
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete all appointments
        Booking_Appointments.objects.all().delete()
        return Response({"message": "All appointments have been deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

# [5.2] ==> Specific Appointment Details asscoiated with (doctor_id) 
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def book_appointment_details(request, doctor_id, pk=None):
    
    try:
        # Fetch all Appointment(s) associated with the given doctor
        book = Booking_Appointments.objects.filter(doctor_id=doctor_id)
        if not book.exists():
            return Response({"error": "No Appointment(s) found for the given doctor ID"}, status=status.HTTP_404_NOT_FOUND)
        
        # If pk is provided, get the specific book from specific doctor's appintment list
        if pk:
            specific_book = get_object_or_404(Booking_Appointments, doctor_id=doctor_id, id=pk)
        
    except ValueError:
        return Response({"error": "Invalid doctor ID or appointment ID :("}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if pk:
            serializer = AppointmentSerializer(specific_book)  # Return specific alarm
        else:
            serializer = AppointmentSerializer(book, many=True)  # Return all user alarms
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT' and pk:
        serializer = AppointmentSerializer(specific_book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment Updated Successfully :)", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' and pk:
        specific_book.delete()
        return Response({"message": "Appointment Deleted Successfully !"}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error": "Can't update or delete all Appointments at the same time :("}, status=status.HTTP_400_BAD_REQUEST)


########################################################################## [Badr's Views] ##################################################################################################################################
########################################################################## [6] Login Api ##################################################################################################################################

# [6.1] ==> Login API
@api_view(['POST'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def custom_user_login(request):
    """
    Login API for the Custom User Model.
    """
    serializer = CustomUserLoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

########################################################################## [7] Previous-History(ies) Api ##################################################################################################################################

# [7.1] ==> Previous History(ies) List
@api_view(['GET', 'POST'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def previous_history_api_view(request):
    
    if request.method == 'GET':
        # Retrieve all histories and serialize them
        histories = PreviousHistory.objects.all().order_by('id')
        serializer = PreviousHistorySerializer(histories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new PreviousHistory instance from the request data
        serializer = PreviousHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# [7.2] ==> Previous History Details
from django.shortcuts import get_object_or_404

@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def previous_history_api_view_details(request, sender_id, pk=None):
    
    try:
        # Fetch all Alarm(s) associated with the given user
        previous = PreviousHistory.objects.filter(sender_id=sender_id)
        if not previous.exists():
            return Response({"error": "No Alarm(s) found for the given user ID"}, status=status.HTTP_404_NOT_FOUND)
        
        # If pk is provided, get the specific previous-history from specific user's previous-history(ies) list
        if pk:
            specific_previous_history = get_object_or_404(PreviousHistory, sender_id=sender_id, id=pk)
            
    except ValueError:
        return Response({"error": "Invalid user ID or Alarm ID :("}, status=status.HTTP_400_BAD_REQUEST)
    

    if request.method == 'GET':
        if pk:
            serializer = PreviousHistorySerializer(specific_previous_history)  # Return specific previous history
        else:
            serializer = PreviousHistorySerializer(previous, many=True)  # Return all user previous histories
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT' and pk:
        serializer = PreviousHistorySerializer(specific_previous_history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Previous history Updated Successfully :)", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' and pk:
        specific_previous_history.delete()
        return Response({"message": "Previous History Deleted Successfully !"}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error": "Can't update or delete all previous history(ies) at the same time :("}, status=status.HTTP_400_BAD_REQUEST)    
########################################################################## [8] Upload-Photo(s) Api ##################################################################################################################################

# [8.1] ==> Upload-Photo(s) List
@api_view(['GET', 'POST', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def upload_photo_api_view_list(request):
    
    upload = UploadedPhoto.objects.all().order_by('id')
    
    if request.method == 'GET':
        serializer = UploadedPhotoSerializer(upload, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
        
    elif request.method == 'POST':
        # Get the user ID from the request data
        user_id = request.data.get('uploader')
        if not user_id:
            return Response(
                {"error": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the user associated with the user ID
            uploader = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User with the given ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is a patient (active=True, staff=False, admin=False)
        if uploader.active and uploader.staff and not uploader.admin:
            serializer = UploadedPhotoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Deny access if the user is not a patient
        return Response(
            {"error": "Only patients & doctors can upload photos !"},
            status=status.HTTP_403_FORBIDDEN
        )

    elif request.method == 'DELETE':
        upload.delete()
        return Response({"message": "All Uploaded Photo(s) deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
# [8.2] ==> Upload-Photo(s) Details
@api_view(['GET', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def upload_photo_api_view_details(request, uploader_id):
    
    try:
        upload = UploadedPhoto.objects.filter(uploader_id=uploader_id)
        if not upload.exists():
            return Response({"error": "No Photo(s) found for the given user ID"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = UploadedPhotoSerializer(upload, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
        
    elif request.method == 'DELETE':
        upload.delete()
        return Response({"message": f"Uploaded Photo deleted successfully !"}, status=status.HTTP_204_NO_CONTENT)

########################################################################## [9] Alarm Api ##################################################################################################################################

# [9.1] ==> Alarm List(s) List
@api_view(['GET', 'POST', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def alram_api_view_list(request):
    
    alarm = Alarm.objects.all().order_by('id')
    if request.method == 'GET':
        serializer = AlarmSerializer(alarm, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
        
    elif request.method == 'POST':
        # Get the user ID from the request data
        user_id = request.data.get('user')
        if not user_id:
            return Response(
                {"error": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the user associated with the user ID
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User with the given ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is a patient (active=True, staff=False, admin=False)
        if user.active and not user.staff and not user.admin:
            serializer = AlarmSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Deny access if the user is not a patient
        return Response(
            {"error": "Only patients can post alarms."},
            status=status.HTTP_403_FORBIDDEN
        )

    elif request.method == 'DELETE':
        alarm.delete()
        return Response({"message": "All alarms deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

# [9.2] ==> Alarm Details
from django.shortcuts import get_object_or_404

@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def alarm_api_view_details(request, user_id, pk=None):
    
    try:
        # Fetch all Alarm(s) associated with the given user
        user_alarms = Alarm.objects.filter(user_id=user_id)
        if not user_alarms.exists():
            return Response({"error": "No Alarm(s) found for the given user ID"}, status=status.HTTP_404_NOT_FOUND)
        
        # If pk is provided, get the specific alarm from specific user's alarm list
        if pk:
            specific_alarm = get_object_or_404(Alarm, user_id=user_id, id=pk)
        
    except ValueError:
        return Response({"error": "Invalid user ID or Alarm ID :("}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if pk:
            serializer = AlarmSerializer(specific_alarm)  # Return specific alarm
        else:
            serializer = AlarmSerializer(user_alarms, many=True)  # Return all user alarms
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT' and pk:
        serializer = AlarmSerializer(specific_alarm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Alarm Updated Successfully :)", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' and pk:
        specific_alarm.delete()
        return Response({"message": "Alarm Deleted Successfully !"}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error": "Can't update or delete all alarms at the same time :("}, status=status.HTTP_400_BAD_REQUEST)
