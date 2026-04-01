from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'city', 'phone', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_active', 'city')
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
