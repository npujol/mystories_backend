from rest_framework import serializers

from ..profiles.serializers import ProfileSerializer
from .models import Comment, Story, Tag
from .relations import TagRelatedField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag", "pk")


class HistorySerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name="get_favorites_count"
    )
    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Story
        fields = (
            "author",
            "body",
            "body_markdown",
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
        author = self.context.get("author", None)
        tags = validated_data.pop("tags", [])
        story = Story.objects.create(author=author, **validated_data)

        for tag in tags:
            obj = Tag.objects.get_or_create(tag=tag)
            story.tags.add(obj)

        return story

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_favorited(self, instance):
        request = self.context.get("request", None)

        if request is None or not request.user.is_authenticated:
            return False

        return request.user.profile.has_favorited(instance)

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    story = HistorySerializer(required=False)
    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Comment
        fields = ("id", "author", "story", "body", "createdAt", "updatedAt")

    def create(self, validated_data):
        story = self.context["story"]
        author = self.context["author"]

        return Comment.objects.create(author=author, story=story, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
