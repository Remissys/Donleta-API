from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
        GETs are public
        POST/PUT/PATCH/DELETE are for admin only 
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        
        return request.user and request.user.is_staff