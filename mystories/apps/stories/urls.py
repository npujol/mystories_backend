from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "stories"

router = DefaultRouter(trailing_slash=False)
router.register("stories", views.StoryViewSet, basename="story")
router.register("tags", views.TagListAPIView, basename="tag")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "stories/<str:story__slug>/favorite",
        views.StoriesFavoriteAPIView.as_view(),
        name="story_favorite",
    ),
    path("stories/feed/", views.StoriesFeedAPIView.as_view(), name="stories_feed_list"),
    path(
        "stories/<str:story__slug>/comments",
        views.CommentsListCreateAPIView.as_view({"get": "list", "post": "create"}),
        name="comment_list",
    ),
    path(
        "stories/<str:story__slug>/comments/<int:pk>",
        views.CommentsRetrieveDestroyAPIView.as_view(
            {"get": "retrieve", "delete": "destroy"}
        ),
        name="comment_detail",
    ),
    path(
        "stories/<str:story__slug>/gtts",
        views.StoryGttsAPIView.as_view({"get": "retrieve", "post": "create_task"}),
        name="story_tts",
    ),
]
