from rest_framework import serializers

from myhistories.apps.profiles.serializers import ProfileSerializer

from .models import History, Comment, Tag
from .relations import TagRelatedField


class HistorySerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name="get_favorites_count"
    )

    tagList = TagRelatedField(many=True, required=False, source="tags")

    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = History
        fields = (
            "author",
            "body",
            "createdAt",
            "description",
            "favorited",
            "favoritesCount",
            "slug",
            "tagList",
            "title",
            "updatedAt",
        )

    def create(self, validated_data):
        author = self.context.get("author", None)

        tags = validated_data.pop("tags", [])

        history = History.objects.create(author=author, **validated_data)

        for tag in tags:
            history.tags.add(tag)

        return history

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_favorited(self, instance):
        request = self.context.get("request", None)

        if request is None:
            return False

        if not request.user.is_authenticated():
            return False

        return request.user.profile.has_favorited(instance)

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)

    createdAt = serializers.SerializerMethodField(method_name="get_created_at")
    updatedAt = serializers.SerializerMethodField(method_name="get_updated_at")

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "body",
            "createdAt",
            "updatedAt",
        )

    def create(self, validated_data):
        history = self.context["history"]
        author = self.context["author"]

        return Comment.objects.create(author=author, history=history, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag",)

    def to_representation(self, obj):
        return obj.tag
