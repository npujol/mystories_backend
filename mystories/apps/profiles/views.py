from django.utils.translation import gettext as _
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..notifications.models import Notification
from .models import Profile
from .serializers import ProfileSerializer


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

    permission_classes = (AllowAny, IsAuthenticated)
    serializer_class = ProfileSerializer

    lookup_field = "user__username"
    queryset = Profile.objects.select_related("user")

    @action(
        detail=True,
        methods=["put"],
        url_path="change_image",
        url_name="change_image",
        permission_classes=[IsAuthenticated],
        parser_classes=[MultiPartParser, FormParser],
    )
    def change_image(self, request, user__username):
        obj = self.get_object()
        obj.image = request.data["image"]
        obj.save()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path="follow_profile",
        url_name="follow_profile",
    )
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

    @action(
        detail=True,
        methods=["delete"],
        url_path="unfollow_profile",
        url_name="unfollow_profile",
    )
    def unfollow_profile(self, request, user__username):
        follower = self.request.user.profile
        followee = self.get_object()
        follower.unfollow(followee)
        serializer = self.serializer_class(followee, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
