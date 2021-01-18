from rest_framework import serializers

from ..authentication.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    image = serializers.FileField(read_only=True)
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("username", "bio", "image", "following")
        read_only_fields = ("username",)

    def get_following(self, profile):
        request = self.context.get("request", None)
        if request is None or not request.user.is_authenticated:
            return False

        follower = request.user.profile

        return follower.is_following(profile)


class ProfileImageSerializer(ProfileSerializer):
    image = serializers.ImageField()

    class Meta(ProfileSerializer.Meta):
        read_only_fields = ("username", "bio", "following")
