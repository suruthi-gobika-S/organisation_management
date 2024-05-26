from rest_framework import viewsets
from .models import Organization, Role, User
from .serializers import OrganizationSerializer, RoleSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsManager, IsMember

def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Example validation logic
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def assign_role_to_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure that the current user has permission to assign roles
    if not request.user.has_perm('orgapp.assign_roles'):
        return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)


    # Assuming you have a way to extract role information from the request data
    role_ids = request.data.get('roles', [])
    roles = Role.objects.filter(id__in=role_ids)

    user.roles.set(roles)
    user.save()

    return Response({"message": "Roles assigned successfully"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()

    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='Manager').exists()

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='Member').exists()

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdmin| IsManager| IsMember]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin | IsManager]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
