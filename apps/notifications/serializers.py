from rest_framework import serializers

from ..profiles.models import Profile
from ..profiles.serializers import ProfileSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    owner = ProfileSerializer(read_only=True)

    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Notification
        fields = (
            "pk",
            "owner",
            "body",
            "title",
            "opened",
            "createdAt",
            "updatedAt",
            "sender",
            "optional",
        )

    def create(self, validated_data):
        owner = self.context.get("author", None)
        return Notification.objects.create(
            owner=owner, status="opened", **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
