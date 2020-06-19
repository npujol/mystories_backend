from django.shortcuts import redirect

from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from ..profiles.models import Profile

from .utils import TTSHistory
from .models import History, Comment, Tag, Speech
from .serializers import HistorySerializer, CommentSerializer, TagSerializer
from .tasks import create_speech


class HistoryViewSet(viewsets.ModelViewSet):
    """
    General ViewSet description

    list: List the histories

    retrieve: Retrieve a history

    update: Update a history

    create: Create a history

    partial_update: Patch a history
    
    destroy: Delete a history

    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = HistorySerializer

    lookup_field = "slug"
    queryset = History.objects.select_related("author", "author__user")

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
        operation_description="Add a favorite to a history",
        responses={404: "slug not found"},
    )
    def post(self, request, history__slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}

        try:
            history = History.objects.get(slug=history__slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug was not found.")

        profile.favorite(history)

        serializer = self.serializer_class(history, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Remove a favorite to a history",
        responses={404: "slug not found"},
    )
    def delete(self, request, history__slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}

        try:
            history = History.objects.get(slug=history__slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug was not found.")

        profile.unfavorite(history)

        serializer = self.serializer_class(history, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HistoriesFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_queryset(self):
        return History.objects.filter(
            author__in=self.request.user.profile.follows.all()
        )


class CommentsListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Comment.objects.select_related(
        "history", "history__author", "history__author__user", "author", "author__user"
    )
    lookup_field = "history__slug"

    def create(self, request, history__slug=None):
        data = request.data
        context = {}

        try:
            context["author"] = Profile.objects.get(user=request.user)
        except History.DoesNotExist:
            raise NotFound("An user with this username does not exist.")

        try:
            context["history"] = History.objects.get(slug=history__slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug does not exist.")

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentsRetrieveDestroyAPIView(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,
):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Comment.objects.select_related(
        "history", "history__author", "history__author__user", "author", "author__user"
    )


class HistoryGttsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HistorySerializer

    @swagger_auto_schema(
        operation_description="Create speech to a history",
        responses={404: "slug not found"},
    )
    def post(self, request, history__slug=None):
        try:
            history = History.objects.get(slug=history__slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug was not found.")

        create_speech.delay(history__slug)

        return Response(
            {"messages": "We are making the speech! we notify you."},
            status=status.HTTP_202_ACCEPTED,
        )

    def get(self, request, history__slug=None):
        try:
            history = History.objects.get(slug=history__slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug was not found.")

        try:
            speech = Speech.objects.get(history=history)
        except Speech.DoesNotExist:
            raise NotFound("A speech with this history was not found.")

        tts = TTSHistory(speech).create()

        if speech.is_ready:
            response = redirect(speech.speech_file.url)
        else:
            response = Response(
                {"state": "Not ready"}, status=status.HTTP_204_NO_CONTENT
            )

        return response
