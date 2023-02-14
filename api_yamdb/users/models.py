from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=settings.ROLE__MAX_LEN,
        choices=ROLE_CHOICES,
        help_text='Назначьте роль пользователя',
        default='user',
    )

    def __str__(self):
        return self.username
