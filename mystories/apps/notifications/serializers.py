from rest_framework import serializers

from ..profiles.models import Profile
from ..profiles.serializers import ProfileSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Notification
        fields = (
            "pk",
            "author",
            "body",
            "title",
            "status",
            "createdAt",
            "updatedAt",
            "receiver",
        )

    def create(self, validated_data):
        author = self.context.get("author", None)
        return Notification.objects.create(
            author=author, status="opened", **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
