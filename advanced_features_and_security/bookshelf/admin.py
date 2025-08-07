from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Custom admin configuration for CustomUser model."""

    # Fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')

    # Fields to filter by in the admin
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')

    # Fields to search by
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Ordering
    ordering = ('username',)

    # Fieldsets for the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    # Fields to include when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

# Register the custom user model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
