from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ..core.permissions import IsOwnerOrReadOnly
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

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = NotificationSerializer

    queryset = Notification.objects.select_related("receiver", "receiver__user")

    def list(self, request, *args, **kwargs):
        receiver = request.user.profile
        print(receiver)
        if receiver is not None:
            self.queryset = self.queryset.filter(receiver=receiver)

        return super().list(self, request, *args, **kwargs)

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"receiver": request.user.profile, "request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
