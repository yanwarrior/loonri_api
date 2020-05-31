from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import UserSerializer, UserRegisterSerializer, SignInSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        raise NotFound(detail='Your request not found')

    def create(self, request, *args, **kwargs):
        raise NotFound(detail='Your request not found')

    def retrieve(self, request, *args, **kwargs):
        raise NotFound(detail='Your request not found')

    def destroy(self, request, *args, **kwargs):
        raise NotFound(detail='Your request not found')

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        email = serializer.data.get('email')

        check_user = User.objects.filter(username=username, email=email)
        if check_user.exists():
            raise ValidationError(detail='User has been registered')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_active = True
        user.save()

        token = Token.objects.create(user=user)

        return Response({
            'username': user.username,
            'email': user.email,
            'token': f'Token {token.key}',
            'is_active': user.is_active
        }, 200)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def sign_in(self, request):
        try:
            serializer = SignInSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            user = User.objects.get(username=username)
            password_check = user.check_password(password)
            if not password_check:
                raise ValidationError('Password does not match!')

            token = Token.objects.get(user=user)
            return Response({
                'username': user.username,
                'email': user.email,
                'token': f'Token {token.key}',
                'is_active': user.is_active
            }, 200)

        except User.DoesNotExist:
            raise ValidationError('User not registered')
        except Exception as e:
            raise ValidationError(e)

    def update(self, request, *args, **kwargs):
        raise NotFound(detail='Your request not found')

    def partial_update(self, request, *args, **kwargs):
        raise NotFound(detail='Your request not found')
