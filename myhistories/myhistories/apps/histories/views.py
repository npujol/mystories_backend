from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import History, Comment, Tag
from .renderers import HistoryJSONRenderer, CommentJSONRenderer
from .serializers import Historieserializer, CommentSerializer, TagSerializer


class HistoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    General ViewSet description

    list: List history

    retrieve: Retrieve history

    update: Update history

    create: Create history

    partial_update: Patch history

    destroy: Delete history
    """

    lookup_field = "slug"
    queryset = History.objects.select_related("author", "author__user")
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (HistoryJSONRenderer,)
    serializer_class = Historieserializer

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
        serializer_context = {"author": request.user.profile, "request": request}
        serializer_data = request.data.get("history", {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {"request": request}
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(page, context=serializer_context, many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug):
        serializer_context = {"request": request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug does not exist.")

        serializer = self.serializer_class(
            serializer_instance, context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        serializer_context = {"request": request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug does not exist.")

        serializer_data = request.data.get("history", {})

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsListCreateAPIView(generics.ListCreateAPIView):
    """
    General ViewSet description

    list: List comment

    retrieve: Retrieve comment

    update: Update comment

    create: Create comment

    partial_update: Patch comment

    destroy: Delete comment
    """

    lookup_field = "history__slug"
    lookup_url_kwarg = "history_slug"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.select_related(
        "history", "history__author", "history__author__user", "author", "author__user"
    )
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def filter_queryset(self, queryset):
        # The built-in list function calls `filter_queryset`. Since we only
        # want comments for a specific history, this is a good place to do
        # that filtering.
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)

    def create(self, request, history_slug=None):
        data = request.data.get("comment", {})
        context = {"author": request.user.profile}

        try:
            context["history"] = History.objects.get(slug=history_slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug does not exist.")

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentsDestroyAPIView(generics.DestroyAPIView):
    """
    General ViewSet description

    list: List comment

    retrieve: Retrieve comment

    update: Update comment

    create: Create comment

    partial_update: Patch comment

    destroy: Delete comment
    """

    lookup_url_kwarg = "comment_pk"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()

    def destroy(self, request, history_slug=None, comment_pk=None):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound("A comment with this ID does not exist.")

        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class HistoriesFavoriteAPIView(APIView):
    """
    General ViewSet description

    list: List history

    retrieve: Retrieve history

    update: Update history

    create: Create history

    partial_update: Patch history

    destroy: Delete history
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (HistoryJSONRenderer,)
    serializer_class = Historieserializer

    def delete(self, request, history_slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}

        try:
            history = History.objects.get(slug=history_slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug was not found.")

        profile.unfavorite(history)

        serializer = self.serializer_class(history, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, history_slug=None):
        profile = self.request.user.profile
        serializer_context = {"request": request}

        try:
            history = History.objects.get(slug=history_slug)
        except History.DoesNotExist:
            raise NotFound("An history with this slug was not found.")

        profile.favorite(history)

        serializer = self.serializer_class(history, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagListAPIView(generics.ListAPIView):
    """
    General ViewSet description

    list: List tag

    retrieve: Retrieve tag

    update: Update tag

    create: Create tag

    partial_update: Patch tag

    destroy: Delete tag
    """

    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def list(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({"tags": serializer.data}, status=status.HTTP_200_OK)


class HistoriesFeedAPIView(generics.ListAPIView):
    """
    General ViewSet description

    list: List history

    retrieve: Retrieve history

    update: Update history

    create: Create history

    partial_update: Patch history

    destroy: Delete history
    """

    permission_classes = (IsAuthenticated,)
    queryset = History.objects.all()
    renderer_classes = (HistoryJSONRenderer,)
    serializer_class = Historieserializer

    def get_queryset(self):
        return History.objects.filter(
            author__in=self.request.user.profile.follows.all()
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {"request": request}
        serializer = self.serializer_class(page, context=serializer_context, many=True)

        return self.get_paginated_response(serializer.data)
