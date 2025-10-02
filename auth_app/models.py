from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username