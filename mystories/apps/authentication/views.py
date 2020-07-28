from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer


class RegistrationAPIView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        responses={404: "slug not found", 201: RegistrationSerializer},
        request_body=RegistrationSerializer,
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginAPIView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        responses={404: "slug not found", 201: LoginSerializer},
        request_body=LoginSerializer,
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(
    viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin
):
    """
    UserRetrieveUpdateAPIView description. It need the username.

    retrieve: Retrieve a user

    update: Update a user

    partial_update: Partial update for a user

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    lookup_field = "username"
    queryset = User.objects.all()
