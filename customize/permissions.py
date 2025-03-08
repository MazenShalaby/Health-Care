from rest_framework.permissions import BasePermission

class CanPostAlarmPermission(BasePermission):
    """
    Custom permission to allow only doctors and patients to post alarms.
    Admins are excluded from posting.
    """
    def has_permission(self, request, view):
        # Allow GET requests for all users
        if request.method == 'GET':
            return True

        # Allow POST requests only for doctors and patients and exclude the admin
        if request.method == 'POST':
            user = request.user
            # Check if the user is a doctor or patient
            if user.active and not user.admin:  # Use `active` and `admin` fields
                if (user.staff and not user.admin) or (not user.staff and not user.admin):
                    return True
            return False

        # Deny all other methods by default
        return False
    
    