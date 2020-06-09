from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related("user")
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    @swagger_auto_schema(
        operation_description="Retrieve the requested profile",
        responses={404: "slug not found"},
    )
    def retrieve(self, request, username, *args, **kwargs):
        # Try to retrieve the requested profile and throw an exception if the
        # profile could not be found.
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist.")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileFollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    @swagger_auto_schema(
        operation_description="Unfallow a profile", responses={404: "slug not found"},
    )
    def delete(self, request, username=None):
        follower = self.request.user.profile

        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username was not found.")

        follower.unfollow(followee)

        serializer = self.serializer_class(followee, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Fallow a profile", responses={404: "slug not found"},
    )
    def post(self, request, username=None):
        follower = self.request.user.profile

        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username was not found.")

        if follower.pk is followee.pk:
            raise serializers.ValidationError("You can not follow yourself.")

        follower.follow(followee)

        serializer = self.serializer_class(followee, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
