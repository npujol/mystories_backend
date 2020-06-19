from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        operation_description="Registration, it need a email and password",
        responses={404: "slug not found"},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="Login, it need username or email, and password ",
        responses={404: "slug not found"},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
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
