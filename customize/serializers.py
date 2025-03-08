from rest_framework import serializers
from . models import (User, Profile, DoctorsProfileInfo, Booking_Appointments, DoctorAvailability, PreviousHistory, UploadedPhoto, Alarm)

########################################################################################################################################################################

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        """
        Hash the password before saving the user instance.
        """
        password = validated_data.pop('password', None)  # Extract the raw password
        user = super().create(validated_data)  # Create the user without the password initially
        if password:
            user.set_password(password)  # Hash the password
            user.save()  # Save the user instance with the hashed password
        return user

    def update(self, instance, validated_data):
        """
        Hash the password if it is updated.
        """
        password = validated_data.pop('password', None)  # Extract the raw password
        instance = super().update(instance, validated_data)  # Update other fields
        if password:
            instance.set_password(password)  # Hash the password
            instance.save()  # Save the user instance with the hashed password
        return instance
        
########################################################################################################################################################################

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
                
########################################################################################################################################################################

class DoctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsProfileInfo
        fields = "__all__"
        
################################################################################################################################################################

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking_Appointments
        fields = '__all__'

    # def create(self, validated_data):
    #     # The clean method in the model ensures validation
    #     return Booking_Appointments.objects.create(**validated_data)
        
################################################################################################################################################################

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'
        
######################################################################### [Badr's Serializers] #######################################################################################        
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate user
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationFailed("This account is inactive.")

        # Add user-specific data
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "profile_picture": user.profile_picture.url if user.profile_picture else None ,
            "age": user.age,
            "gender": user.gender,
            "chronic_disease": user.chronic_disease,
            "token": user.auth_token.key,
            "staff": user.is_staff,
            "active": user.is_active,
            "cancer_type": user.cancer_type,
            "cancer_photo": user.cancer_photo.url if user.cancer_photo else None,
            "cancer_percentage": user.cancer_percentage,
        }
###############################################################################

class PreviousHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousHistory
        fields = '__all__'

###############################################################################

class UploadedPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPhoto
        fields = '__all__'
        
###############################################################################

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'