from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

# from users.validators import validate_username # validate_username_exists

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
    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'token')

    def create(self, validated_data):
        return User.objects.get_or_create(**validated_data)

#   def validate_confirmation_code(self, value):
#       if self.context['request'].user.confirmation_code != value:
#           raise ValidationError('Код подтверждения не совпадает!')
#       return value
        # user = CurrentUserDefault()
        # if user.confirmation_code != value:
