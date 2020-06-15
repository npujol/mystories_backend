from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

app_name = "histories"

router = DefaultRouter(trailing_slash=False)
router.register("histories", views.HistoryViewSet, basename="history")
router.register("tags", views.TagListAPIView, basename="tag")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "histories/<str:history__slug>/favorite/",
        views.HistoriesFavoriteAPIView.as_view(),
        name="history_favorite",
    ),
    path(
        "histories/feed/",
        views.HistoriesFeedAPIView.as_view(),
        name="histories_feed_list",
    ),
    path(
        "histories/<str:history__slug>/comments",
        views.CommentsListCreateAPIView.as_view({"get": "list", "post": "create"}),
        name="comment_list",
    ),
    path(
        "histories/<str:history__slug>/comments/<int:pk>",
        views.CommentsRetrieveDestroyAPIView.as_view(
            {"get": "retrieve", "delete": "destroy"}
        ),
        name="comment_detail",
    ),
    path(
        "histories/<str:history__slug>/gtts",
        views.HistoryGttsAPIView.as_view(),
        name="history_tts",
    ),
]
