from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # ✅ Import your custom manager

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    objects = CustomUserManager()  # ✅ Attach your custom manager

    def __str__(self):
        return self.username
