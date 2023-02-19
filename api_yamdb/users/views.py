from secrets import randbelow

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_400_BAD_REQUEST

from users.serializers import (GettingTokenSerializer, SignUpSerializer,
                               UserSerializer)

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ['get', 'post']
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch', 'delete'],
            url_path=r'(?P<username>^[\w.@+-]+)')
    def user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(data=request.data)
    #    serializer = self.get_serializer(user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        owner = self.request.user
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.method == 'get':
            return Response(serializer.data)
        serializer.save(role=owner.role)
        return Response(serializer.data)


@api_view(['POST'])
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


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)
    serializer = GettingTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
#    data = serializer.validated_data  #
    if request.data.get('confirmation_code') == user.confirmation_code:  #
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response(data={'token': token})
    return Response(
        {'confirmation_code': 'Код подтверждения не совпадает!'},
        status=HTTP_400_BAD_REQUEST
    )
