from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='адрес электропочты',
        help_text='введите адрес электрической почты'
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Token',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []