from rest_framework import serializers

from ..authentication.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), read_only=False
    )
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "user",
            "bio",
            "image",
            "following",
        )
        read_only_fields = ("user",)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return "https://static.productionready.io/images/smiley-cyrus.jpg"

    def get_following(self, instance):
        request = self.context.get("request", None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        follower = request.user.profile
        followee = instance

        return follower.is_following(followee)
