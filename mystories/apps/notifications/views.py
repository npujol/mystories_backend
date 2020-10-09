from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
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
        opened = self.request.query_params.get("opened", None)
        receiver = request.user.profile
        if receiver is not None and opened is not None:
            self.queryset = self.queryset.filter(receiver=receiver, opened=opened)
        elif receiver is not None:
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

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def openedStatus(self, request, pk):
        opened = self.request.data
        print(opened)
        notification = self.get_object()
        notification.opened = opened
        notification.save()
        serializer = self.serializer_class(notification, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
