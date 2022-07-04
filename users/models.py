from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(null=True)
    gender = models.CharField(
        max_length=1, choices=[("M", "Male"), ("F", "Female")], null=True
    )
