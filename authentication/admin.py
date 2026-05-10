# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserModelAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'phone', 'credits', 'is_superuser', 'is_staff',)
    search_fields = ('username', 'email', 'phone')
    ordering = ('email',) 

    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone', 'credits', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(User, UserModelAdmin)
