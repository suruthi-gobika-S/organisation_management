from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, RoleViewSet, UserViewSet
from . import views

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/assign-role/<int:user_id>/', views.assign_role_to_user, name='user-assign-role'),
]

