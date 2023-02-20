import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# from users.models import User


def validate_username(value):
    if value == 'me':
        raise ValidationError('Этот ник зарезеривирован')
    pattern = re.compile(r'^[\w.@+-]+')
    if not pattern.match(value):
        raise ValidationError(
            'Можно использовать только цифры, буквы и символы @/./+/-/_'
        )


# def validate_username_exists(value):
#    if User.objects.filter(username=value).exists():
#        raise ValidationError('Этот ник уже занят')


#def validate_email_exists(value):
#    if User.objects.filter(email=value).exists():
#        raise ValidationError('Эта почта уже была использована')
