from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('resident', 'Resident'),
        ('entrepreneur', 'Entrepreneur'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')

    # Email is required to create a user in addition to username
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


