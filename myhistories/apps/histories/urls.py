from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    HistoryViewSet,
    HistoriesFavoriteAPIView,
    HistoriesFeedAPIView,
    CommentsListCreateAPIView,
    CommentsRetrieveDestroyAPIView,
    TagListAPIView,
)

app_name = "histories"

router = DefaultRouter(trailing_slash=False)
router.register("api/histories", HistoryViewSet, basename="history")
router.register("api/tags", TagListAPIView, basename="tag")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "api/histories/<str:history__slug>/favorite/",
        HistoriesFavoriteAPIView.as_view(),
        name="history_favorite",
    ),
    path(
        "api/histories/feed/",
        HistoriesFeedAPIView.as_view(),
        name="histories_feed_list",
    ),
    path(
        "api/<str:history__slug>/comments",
        CommentsListCreateAPIView.as_view({"get": "list", "post": "create"}),
        name="comment_list",
    ),
    path(
        "api/histories/<str:history__slug>/comments/<int:pk>",
        CommentsRetrieveDestroyAPIView.as_view(
            {"get": "retrieve", "delete": "destroy"}
        ),
        name="comment_detail",
    ),
]
