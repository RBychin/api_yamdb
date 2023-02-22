from secrets import randbelow

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from .permissions import IsAdminUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.status import HTTP_400_BAD_REQUEST

from users.serializers import (GettingTokenSerializer, SignUpSerializer,
                               UserSerializer)

User = get_user_model()


class UserViewSet(ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=(['get', 'patch', 'delete']),
        permission_classes=[IsAuthenticated],
    )
    def user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
    #    serializer = UserSerializer(data=request.data)
        serializer = self.get_serializer(user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=(['get', 'patch']),
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        owner = request.user
        if request.method == 'get':
            serializer = self.get_serializer(owner)
            return Response(serializer.data)
    #    serializer = UserSerializer(data=request.data, partial=True)
        serializer = self.get_serializer(
            owner,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=owner.role)
        return Response(serializer.data)


@api_view(['post'])
@permission_classes([AllowAny])
def sign_up(request):
    username = request.data.get('username')
    email = request.data.get('email')
    if User.objects.filter(username=username, email=email).exists():
        user, created = User.objects.get_or_create(username=username)
        if not created:
            confirmation_code = randbelow(settings.CONF_CODE_RANGE_UPP_LIMIT)
            user.confirmation_code = confirmation_code
            send_mail(
                subject='Новый код подтверждения',
                message=f'Новый код подтверждения - {str(confirmation_code)} ',
                from_email=None,
                recipient_list=(email,)
            )
            user.save()
            return Response('Код подтверждения обновлен')
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = randbelow(settings.CONF_CODE_RANGE_UPP_LIMIT)
    email = serializer.validated_data.get('email')
    send_mail(
        subject='Код подтверждения',
        message=f'Код подтверждения - {str(confirmation_code)} ',
        from_email=None,
        recipient_list=(email,)
    )
    serializer.save(confirmation_code=confirmation_code)
    return Response(request.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GettingTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
