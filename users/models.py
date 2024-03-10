from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, null=True, blank=True, verbose_name='телефон')
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='аватар')
    telegram_id = models.CharField(max_length=11, null=True, blank=True, verbose_name='телеграм-id')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
