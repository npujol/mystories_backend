from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from ..profiles.models import Profile
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    General ViewSet description

    list: List the notifications

    retrieve: Retrieve a notification

    update: Update a notification

    create: Create a notification

    partial_update: Patch a notification

    destroy: Delete a notification

    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = NotificationSerializer

    queryset = Notification.objects.select_related("author", "author__user")

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"author": request.user.profile, "request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
