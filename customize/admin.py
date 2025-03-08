from django.contrib import admin
from django import forms
from .models import (
    Profile, DoctorsProfileInfo, Booking_Appointments, 
    PreviousHistory, UploadedPhoto, DoctorAvailability, Alarm
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

# Get the custom User model
User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'created_at', 'last_login', 'admin', 'staff', 'active', 'phone', 'cancer_type', 'cancer_percentage']
    list_filter = ['active', 'staff', 'admin']
    search_fields = ['email', 'full_name', 'phone']
    ordering = ['email']

    fieldsets = (
        ('Authentication', {'fields': ('email', 'password')}),
        
        ('Personal Information', {
            'fields': ('full_name', 'first_name', 'last_name', 'phone', 'age', 'gender', 'chronic_disease')
        }),
        
        ('Cancer Information', {
            'fields': ('cancer_type', 'cancer_photo', 'cancer_percentage')}),
        
        ('Permissions', {'fields': ('active', 'staff', 'admin')}),
    )

    add_fieldsets = (
        ('Registeration', {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'full_name', 'first_name', 'last_name', 'age', 'gender', 'chronic_disease', 'phone', 'profile_picture'
            ),
        }),
    )

    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for UserAdmin.
        """
        super().save_model(request, obj, form, change)

        # Create or update Profile for non-admin, non-staff users (patients)
        if obj.active and not obj.is_admin and not obj.is_staff:
            profile, created = Profile.objects.get_or_create(user=obj)
            profile.first_name = obj.first_name
            profile.last_name = obj.last_name
            profile.phone = obj.phone
            profile.age = obj.age
            profile.gender = obj.gender
            profile.chronic_disease = obj.chronic_disease
            profile.save()
        else:
            # Delete Profile if user is promoted to admin or staff
            if hasattr(obj, 'profile') and obj.profile.id is not None:  # Check if profile exists
                obj.profile.delete()

# Register the custom UserAdmin
admin.site.register(User, UserAdmin)
# Unregister the Group model
admin.site.unregister(Group)

#############################################################################################################

# DoctorsProfileInfo Admin
class DoctorsProfileInfoAdmin(admin.ModelAdmin):
    search_fields = ['doc_first_name', 'doc_last_name', 'phone', 'specialty']
    list_display = ['doc_first_name', 'doc_last_name', 'specialty', 'phone']
    ordering = ['doc_last_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filter the 'user' field to show only available users with the correct permissions.
        """
        if db_field.name == "user":
            used_users = DoctorsProfileInfo.objects.values_list('user', flat=True)
            kwargs["queryset"] = User.objects.filter(admin=False, staff=True, active=True)#.exclude(id__in=used_users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(DoctorsProfileInfo, DoctorsProfileInfoAdmin)

#############################################################################################################

# PreviousHistory Admin

class PreviousHistoryAdminForm(forms.ModelForm):
    class Meta:
        model = PreviousHistory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter sender field to show only doctors (staff=True and active=True)
        self.fields['sender'].queryset = User.objects.filter(admin=False, staff=True, active=True)

        # Filter receiver field to show only patients (admin=False, staff=False, active=True)
        self.fields['receiver'].queryset = User.objects.filter(admin=False, staff=False, active=True)

class PreviousHistoryAdmin(admin.ModelAdmin):
    form = PreviousHistoryAdminForm
    list_display = ('sender', 'receiver', 'message', 'date', 'time')
    list_filter = ('sender', 'receiver', 'date', 'time')  # Optional: Add filters for admin view
    search_fields = ('sender__email', 'reciever__email', 'message')  # Optional: Add search functionality

admin.site.register(PreviousHistory, PreviousHistoryAdmin)

#############################################################################################################

class AlarmAdminForm(forms.ModelForm):
    class Meta:
        model = Alarm
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter user field to show [patients] => (admin=False, staff=True, active=True) & [patients] => (admin=False, staff=False, active=True)
        self.fields['user'].queryset = User.objects.filter(admin=False, staff=False, active=True)

class AlarmAdmin(admin.ModelAdmin):
    form = AlarmAdminForm
    list_display = ('user', 'pill_name', 'alarm_time', 'created_at')
    list_filter = ('user', 'alarm_time', 'created_at')  # Optional: Add filters for admin view
    search_fields = ('user__email', 'pill_name')  # Optional: Add search functionality

admin.site.register(Alarm, AlarmAdmin)

#############################################################################################################
# Appointment Admin
from django.core.exceptions import ValidationError
from django.db.models import Q

class BookAppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time', 'available']
    search_fields = ['patient__email']
    ordering = ['date', 'time']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filter the 'patient' field to show only users with the correct permissions.
        """
        if db_field.name == "patient":
            kwargs["queryset"] = User.objects.filter(admin=False, staff=False, active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Prevent double-booking: Ensure no other appointment exists 
        with the same doctor, date, and time before saving.
        """
        if Booking_Appointments.objects.filter(
            Q(doctor=obj.doctor) & 
            Q(date=obj.date) & 
            Q(time=obj.time) & 
            ~Q(id=obj.id)  # Exclude the current object if updating [blocks double-booking for new appointments but allows updates to existing ones.]
        ).exists():
            raise ValidationError("This appointment slot is already booked by another patient.")

        obj.available = False
        super().save_model(request, obj, form, change)

admin.site.register(Booking_Appointments, BookAppointmentAdmin)

#############################################################################################################

# DoctorAvailability Admin
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor','start_time','end_time']
    list_filter = ['doctor']
    search_fields = ['doctor__doc_first_name', 'doctor__doc_last_name']
    ordering = ['doctor']
    list_per_page = 10  # Optional: Controls how many items to display per page
    
    # Customizing the form to filter doctors based on specific permissions
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            # Only allow doctors that have the correct permissions
            kwargs["queryset"] = DoctorsProfileInfo.objects.filter(user__admin=False, user__staff=True, user__active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for DoctorAvailability.
        - Ensure the validation for start and end time is applied.
        - You can add more custom logic here if needed.
        """
        obj.clean()  # Make sure custom validation is triggered
        super().save_model(request, obj, form, change)

admin.site.register(DoctorAvailability, DoctorAvailabilityAdmin)

#############################################################################################################

# Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone', 'age', 'gender', 'chronic_disease']
    list_filter = ['gender', 'age']
    search_fields = ['user__email', 'first_name', 'last_name', 'phone']
    ordering = ['user']
    list_per_page = 10  # Optional: Controls how many items to display per page

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for Profile.
        - Ensure that any necessary validation or additional logic is triggered.
        """
        # Custom logic can be added here if needed
        super().save_model(request, obj, form, change)

admin.site.register(Profile, ProfileAdmin)

#############################################################################################################

class PhotoUploaderAdminForm(forms.ModelForm):
    class Meta:
        model = UploadedPhoto
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter uploader field to show only doctors and patients (admin=False, staff=True , active=True) => doctor or (admin=False, staff=False, active=True) => patient
        self.fields['uploader'].queryset = User.objects.filter(admin=False, staff=True, active=True) | User.objects.filter(admin=False, staff=False, active=True)
        
        
class PhotoUploaderAdmin(admin.ModelAdmin):
    
    form = PhotoUploaderAdminForm
    list_display = ['uploader','submitted_date', 'confidence_score',  'timestamp', 'updated_at']
    list_filter = ['timestamp']  # Optional: Add filters for admin view
    search_fields = ['uploader']  # Optional: Add search functionality
        
# Register other models
admin.site.register(UploadedPhoto, PhotoUploaderAdmin)