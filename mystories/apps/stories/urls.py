from django.conf.urls import include
from django.urls import path
from rest_framework_nested import routers

from . import views

app_name = "stories"

router = routers.DefaultRouter(trailing_slash=False)
router.register("stories", views.StoryViewSet, basename="story")
router.register("tags", views.TagListAPIView, basename="tag")

stories_router = routers.NestedSimpleRouter(router, "stories", lookup="story")
stories_router.register("comments", views.CommentsAPIView, basename="story_comment")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(stories_router.urls)),
    path("stories/feed/", views.StoriesFeedAPIView.as_view(), name="stories_feed_list"),
]
