from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..notifications.models import Notification
from .models import Profile
from .serializers import ProfileSerializer


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    ProfileRetrieveUpdateAPIView description. It need a username.

    retrieve: Retrieve a profile

    update: Update a profile

    partial_update: Partial update for a profile

    """

    permission_classes = (AllowAny, IsAuthenticated)
    serializer_class = ProfileSerializer

    lookup_field = "user__username"
    queryset = Profile.objects.select_related("user")


class ProfileFollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    lookup_field = "user__username"

    @swagger_auto_schema(
        operation_description="Follow a profile. It need a username for the profile to follow",
        responses={404: "slug not found"},
    )
    def post(self, request, user__username=None):
        follower = self.request.user.profile

        try:
            followee = Profile.objects.get(user__username=user__username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username was not found.")

        if follower.pk is followee.pk:
            raise serializers.ValidationError("You can not follow yourself.")

        follower.follow(followee)
        serializer = self.serializer_class(followee, context={"request": request})

        Notification.objects.create(
            title=_("You have a new follower"),
            body=_("{} follows you!".format(follower)),
            author=follower,
            receiver=followee,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Unfollow a profile. It need a username for the profile to follow",
        responses={404: "slug not found"},
    )
    def delete(self, request, user__username=None):
        follower = self.request.user.profile

        try:
            followee = Profile.objects.get(user__username=user__username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username was not found.")

        follower.unfollow(followee)
        serializer = self.serializer_class(followee, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
