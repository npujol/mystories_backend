from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..core.permissions import IsOwner, IsOwnerOrReadOnly
from ..notifications.models import Notification
from ..profiles.models import Profile
from .models import Comment, Speech, Story, Tag
from .serializers import (
    CommentSerializer,
    SpeechSerializer,
    StoryImageSerializer,
    StoryPrivateSerializer,
    StorySerializer,
    TagSerializer,
)
from .tasks import create_speech
from .utils import TTSStory


class StoryViewSet(viewsets.ModelViewSet):
    """
    General ViewSet description

    list: List the stories

    retrieve: Retrieve a story

    update: Update a story

    create: Create a story

    partial_update: Patch a story

    destroy: Delete a story

    """

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = StorySerializer

    lookup_field = "slug"
    queryset = Story.objects.select_related("author", "author__user")

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["author__user__username", "tags__tag", "author__favorites"]

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get("author", None)
        favorited_by = self.request.query_params.get("favorited", None)
        tag = self.request.query_params.get("tag", None)

        if author is not None:
            return queryset.filter(author__user__username=author)

        if tag is not None:
            return queryset.filter(tags__tag=tag)

        if favorited_by is not None:
            return queryset.filter(favorited_by__user__username=favorited_by)
        return queryset

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"author": request.user.profile, "request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsOwner],
        serializer_class=StoryPrivateSerializer,
    )
    def get_body_markdown(self, request, slug=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["put"],
        permission_classes=[IsOwner],
        parser_classes=[MultiPartParser],
        serializer_class=StoryImageSerializer,
    )
    def change_image(self, request, slug=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}
        story = self.get_object()
        profile.favorite(story)

        Notification.objects.create(
            title=_("Your story was marked as a favorite."),
            body=_("{} marks your story: {} as favorite".format(profile, story)),
            author=profile,
            receiver=story.author,
        )

        serializer = self.serializer_class(story, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unfavorite(self, request, slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}
        story = self.get_object()

        profile.unfavorite(story)
        serializer = self.serializer_class(story, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def make_audio(self, request, slug=None):
        story = self.get_object()

        try:
            speech = Speech.objects.get(story=story)

            return Response(
                {"message": "This story has a speech already"},
                status=status.HTTP_202_ACCEPTED,
            )
        except Speech.DoesNotExist:

            create_speech.delay(slug)

            return Response(
                {"message": "We are making the speech! We will notify you."},
                status=status.HTTP_202_ACCEPTED,
            )

    @action(detail=True, methods=["get"])
    def get_audio(self, request, slug=None):
        story = self.get_object()
        speech = get_object_or_404(Speech, story=story)

        return Response(SpeechSerializer(speech).data, status=status.HTTP_200_OK)


class TagListAPIView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    General ViewSet description

    list: List the tags

    retrieve: Retrieve a tag

    create: Create a tag

    destroy: Delete a tag

    """

    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class StoriesFeedAPIView(generics.ListAPIView):
    """
    General ViewSet description

    list: List the Stories
    """

    permission_classes = (AllowAny,)
    serializer_class = StorySerializer
    queryset = Story.objects.all()


class CommentsAPIView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    General ViewSet description

    list: List the comments

    create: Create a comment

    retrieve: Retrieve a comment

    destroy: Delete a comment

    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.select_related("story")

    def get_queryset(self):
        queryset = self.queryset
        slug = self.kwargs["story_slug"]
        if slug:
            return queryset.filter(story__slug=slug)

        return queryset

    def create(self, request, story_slug=None):
        data = request.data
        context = {}

        author = get_object_or_404(Profile, user=request.user)
        story = get_object_or_404(Story, slug=story_slug)

        context["author"] = author
        context["story"] = story

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        Notification.objects.create(
            title=_("Your story has a new comment."),
            body=_("{} comment in your story {}".format(author, story)),
            author=author,
            receiver=story.author,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
