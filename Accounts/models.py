from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('business', 'Business'),
    )
    phone_number = models.CharField(max_length=15, unique = True)

    user_type = models.CharField(max_length= 10, choices = USER_TYPE_CHOICES)

    def __str__ (self):
        return f"{self.username}  ({self.user_type})"



