from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..notifications.models import Notification
from ..profiles.models import Profile
from .models import Comment, Speech, Story, Tag
from .serializers import CommentSerializer, HistorySerializer, TagSerializer
from .tasks import create_speech
from .utils import TTSHistory


class HistoryViewSet(viewsets.ModelViewSet):
    """
    General ViewSet description

    list: List the stories

    retrieve: Retrieve an story

    update: Update an story

    create: Create an story

    partial_update: Patch an story

    destroy: Delete an story

    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = HistorySerializer

    lookup_field = "slug"
    queryset = Story.objects.select_related("author", "author__user")

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get("author", None)

        if author is not None:
            queryset = queryset.filter(author__user__username=author)

        tag = self.request.query_params.get("tag", None)

        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        favorited_by = self.request.query_params.get("favorited", None)

        if favorited_by is not None:
            queryset = queryset.filter(favorited_by__user__username=favorited_by)

        return queryset

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"author": request.user.profile, "request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagListAPIView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class HistoriesFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HistorySerializer

    @swagger_auto_schema(
        operation_description="Add a favorite to an story",
        responses={404: "slug not found", 201: HistorySerializer},
        request_body=HistorySerializer,
    )
    def post(self, request, history__slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}

        story = get_object_or_404(Story, slug=history__slug)

        profile.favorite(story)

        Notification.objects.create(
            title=_("Your story was marked as a favorite."),
            body=_("{} marks your story: {} as favorite".format(profile, story)),
            author=profile,
            receiver=story.author,
        )

        serializer = self.serializer_class(story, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Remove a favorite to an story",
        responses={404: "slug not found", 201: HistorySerializer},
        request_body=HistorySerializer,
    )
    def delete(self, request, history__slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}

        story = get_object_or_404(Story, slug=history__slug)

        profile.unfavorite(story)

        serializer = self.serializer_class(story, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HistoriesFeedAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Story.objects.all()
    serializer_class = HistorySerializer


class CommentsListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Comment.objects.select_related(
        "story", "history__author", "history__author__user", "author", "author__user"
    )
    lookup_field = "history__slug"

    def create(self, request, history__slug=None):
        data = request.data
        context = {}

        author = get_object_or_404(Profile, user=request.user)
        story = get_object_or_404(Story, slug=history__slug)

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


class CommentsRetrieveDestroyAPIView(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Comment.objects.select_related(
        "story", "history__author", "history__author__user", "author", "author__user"
    )


class HistoryGttsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HistorySerializer

    @swagger_auto_schema(
        operation_description="Create speech to an story",
        responses={404: "slug not found", 201: HistorySerializer},
        request_body=HistorySerializer,
    )
    def post(self, request, history__slug=None):
        story = get_object_or_404(Story, slug=history__slug)

        try:
            speech = Speech.objects.get(story=story)

            return Response(
                {"message": "This story has a speech already"},
                status=status.HTTP_202_ACCEPTED,
            )
        except Speech.DoesNotExist:

            create_speech.delay(history__slug)

            return Response(
                {"message": "We are making the speech! We will notify you."},
                status=status.HTTP_202_ACCEPTED,
            )

    def get(self, request, history__slug=None):
        story = get_object_or_404(Story, slug=history__slug)
        speech = get_object_or_404(Speech, story=story)

        if speech.is_ready:
            return redirect(speech.speech_file.url)

        return Response({"message": "Not ready"})
