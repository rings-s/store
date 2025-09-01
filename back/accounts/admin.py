from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name', 
        'role', 'is_active', 'is_staff', 
        'created_at', 'loyalty_points'
    )
    list_filter = (
        'role', 'is_active', 'is_staff', 
        'is_superuser', 'created_at'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'phone_number', 
                'avatar', 'bio'
            )
        }),
        ('Address Information', {
            'fields': (
                'street_address', 'city', 'state', 
                'postal_code', 'country'
            )
        }),
        ('Role & Permissions', {
            'fields': (
                'role', 'is_active', 
                'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Preferences', {
            'fields': (
                'preferred_currency', 'language_preference', 
                'loyalty_points'
            )
        }),
        ('Important Dates', {
            'fields': ('created_at',)
        }),
    )
    
    add_fieldsets = (
        ('Authentication', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff')
        }),
    )
    
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"


