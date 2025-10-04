from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'company', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff', 'company']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['email']
    
    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Company & Role', {
            'fields': ('company', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Authentication', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Company & Role', {
            'fields': ('company', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
