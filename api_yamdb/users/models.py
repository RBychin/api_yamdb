from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'Ник',
        unique=True,
        max_length=settings.USERNAME_MAX_LEN,
        validators=[validate_username]
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=settings.ROLE_MAX_LEN,
        choices=ROLE_CHOICES,
        help_text='Назначьте роль пользователя',
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.CONF_CODE_MAX_LEN,
        blank=True,
        default='null',
    )
    token = models.TextField(
        'Токен',
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id', ]
