from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .renderers import UserJSONRenderer
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        operation_description="Make a new email registration",
        responses={404: "slug not found"},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
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
    RetrieveUpdateAPIView description

    retrieve: Retrieve history

    update: Update history

    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def update(self, request, *args, **kwargs):
    #     user_data = request.data
    #     print(user_data.get("profile")["bio"])
    #     serializer_data = {
    #         "username": user_data.get("username"),
    #         "email": user_data.get("email"),
    #         "profile": {
    #             "bio": user_data.get("profile")["bio"],
    #             "image": user_data.get("profile")["image"],
    #         },
    #     }

    #     serializer = self.serializer_class(
    #         request.user, data=serializer_data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)
