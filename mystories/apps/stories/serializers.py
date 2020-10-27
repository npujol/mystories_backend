from rest_framework import serializers

from ..core.serializer_fields import AddObjectSlugRelatedField
from ..profiles.serializers import ProfileSerializer
from .models import Comment, Speech, Story, Tag
from .relations import TagRelatedField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag", "pk")


class StoryPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ("body_markdown",)


class StorySerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    tags = AddObjectSlugRelatedField(
        slug_field="tag", queryset=Tag.objects.all(), many=True
    )
    image = serializers.FileField(read_only=True)

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name="get_favorites_count"
    )
    body = serializers.CharField(read_only=True)
    body_markdown = serializers.CharField(write_only=True)
    hadAudio = serializers.SerializerMethodField(method_name="had_audio")
    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Story
        fields = (
            "owner",
            "body",
            "body_markdown",
            "hadAudio",
            "language",
            "image",
            "description",
            "favorited",
            "favoritesCount",
            "slug",
            "tags",
            "title",
            "createdAt",
            "updatedAt",
        )

    def create(self, validated_data):
        owner = self.context.get("author", None)
        tags = validated_data.pop("tags", [])
        story = Story.objects.create(owner=owner, **validated_data)

        for tag in tags:
            story.tags.add(tag)

        return story

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", [])
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        instance = super(StorySerializer, self).update(instance, validated_data)
        return instance

    def get_favorited(self, instance):
        request = self.context.get("request", None)

        if request is None or not request.user.is_authenticated:
            return False

        return request.user.profile.has_favorited(instance)

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def had_audio(self, instance):
        return Speech.objects.filter(story=instance).exists()


class StoryImageSerializer(StorySerializer):
    image = serializers.ImageField()

    class Meta(StorySerializer.Meta):
        fields = (
            "owner",
            "body",
            "language",
            "image",
            "description",
            "hadAudio",
            "favorited",
            "favoritesCount",
            "slug",
            "title",
            "createdAt",
            "updatedAt",
        )
        read_only_fields = (
            "owner",
            "body",
            "language",
            "description",
            "hadAudio",
            "favorited",
            "favoritesCount",
            "slug",
            "title",
            "createdAt",
            "updatedAt",
        )


class CommentSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(required=False)
    story = StorySerializer(required=False)
    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Comment
        fields = ("id", "owner", "story", "body", "createdAt", "updatedAt")

    def create(self, validated_data):
        story = self.context["story"]
        owner = self.context["author"]

        return Comment.objects.create(owner=owner, story=story, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class SpeechSerializer(serializers.ModelSerializer):
    story = StorySerializer(read_only=True, required=False)
    language = serializers.CharField(required=False)
    speech_file = serializers.SerializerMethodField(method_name="speech_file_abs")
    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Speech
        fields = ("pk", "story", "language", "speech_file", "createdAt", "updatedAt")

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def speech_file_abs(self, instance):
        return self.context["request"].build_absolute_uri(instance.speech_file.url)
