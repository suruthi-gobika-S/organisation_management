from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """
    Allows access only to superadmin users.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='Manager').exists()

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='Member').exists()
