import re

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'confirmation_code')

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)


class GettingTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'token')

#   def validate_confirmation_code(self, value):
#       if self.context['request'].user.confirmation_code != value:
#           raise ValidationError('Код подтверждения не совпадает!')
#       return value
        # user = CurrentUserDefault()
        # if user.confirmation_code != value:
