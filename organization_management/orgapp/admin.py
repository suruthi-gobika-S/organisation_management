#from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'organization', 'is_staff', 'is_superuser')

admin.site.register(User, CustomUserAdmin)

# Register your models here.
