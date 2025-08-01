from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

<<<<<<< HEAD
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
=======
admin.site.register(CustomUser, UserAdmin)
>>>>>>> 1183f4dbd27881de986d484e1ab05adeaf90ff74
