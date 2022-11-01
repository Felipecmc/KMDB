from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=127, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    bio = models.TextField(null=True)
    is_critic = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    REQUIRED_FIELDS = ["email", "password", "birthdate","first_name", "last_name"]
    
