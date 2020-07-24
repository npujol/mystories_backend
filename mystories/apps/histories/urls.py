from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "stories"

router = DefaultRouter(trailing_slash=False)
router.register("stories", views.HistoryViewSet, basename="story")
router.register("tags", views.TagListAPIView, basename="tag")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "stories/<str:history__slug>/favorite/",
        views.HistoriesFavoriteAPIView.as_view(),
        name="history_favorite",
    ),
    path(
        "stories/feed/",
        views.HistoriesFeedAPIView.as_view(),
        name="histories_feed_list",
    ),
    path(
        "stories/<str:history__slug>/comments",
        views.CommentsListCreateAPIView.as_view({"get": "list", "post": "create"}),
        name="comment_list",
    ),
    path(
        "stories/<str:history__slug>/comments/<int:pk>",
        views.CommentsRetrieveDestroyAPIView.as_view(
            {"get": "retrieve", "delete": "destroy"}
        ),
        name="comment_detail",
    ),
    path(
        "stories/<str:history__slug>/gtts",
        views.HistoryGttsAPIView.as_view(),
        name="history_tts",
    ),
]
