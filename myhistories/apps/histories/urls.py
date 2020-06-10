from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import (
    HistoryViewSet,
    HistoriesFavoriteAPIView,
    HistoriesFeedAPIView,
    CommentsListCreateAPIView,
    CommentsDestroyAPIView,
    TagListAPIView,
)

app_name = "histories"

router = DefaultRouter(trailing_slash=False)
router.register(r"histories", HistoryViewSet, basename="history")

urlpatterns = [
    url(r"^", include(router.urls)),
    url(
        r"^histories/feed/?$",
        HistoriesFeedAPIView.as_view(),
        name="histories_feed_list",
    ),
    url(
        r"^histories/(?P<article_slug>[-\w]+)/favorite/?$",
        HistoriesFavoriteAPIView.as_view(),
        name="history_favorite",
    ),
    url(
        r"^histories/(?P<article_slug>[-\w]+)/comments/?$",
        CommentsListCreateAPIView.as_view(),
        name="comments",
    ),
    url(
        r"^histories/(?P<article_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$",
        CommentsDestroyAPIView.as_view(),
        name="remove_comment",
    ),
    url(r"^tags/?$", TagListAPIView.as_view(), name="tags"),
]
