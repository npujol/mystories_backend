from django.utils.translation import gettext as _
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from ..notifications.models import Notification
from .models import Profile
from .serializers import ProfileImageSerializer, ProfileSerializer


class ProfileRetrieveUpdateAPIView(
    viewsets.GenericViewSet,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin,
):
    """
    General description. It need a username.

    retrieve: Retrieve a profile

    update: Update a profile

    partial_update: Partial update for a profile

    """

    permission_classes = (AllowAny, IsAuthenticatedOrReadOnly)
    serializer_class = ProfileSerializer

    lookup_field = "user__username"
    queryset = Profile.objects.select_related("user")

    @action(
        detail=True,
        methods=["put"],
        permission_classes=[IsAuthenticated],
        parser_classes=[MultiPartParser],
        serializer_class=ProfileImageSerializer,
    )
    def change_image(self, request, user__username):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def follow_profile(self, request, user__username):
        follower = self.request.user.profile
        followee = self.get_object()

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

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unfollow_profile(self, request, user__username):
        follower = self.request.user.profile
        followee = self.get_object()
        follower.unfollow(followee)
        serializer = self.serializer_class(followee, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
