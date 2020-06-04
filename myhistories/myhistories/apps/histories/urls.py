from django.conf.urls import url
from django.urls import include, path


from rest_framework.routers import SimpleRouter

from .views import (
    HistoryViewSet,
    HistoriesFavoriteAPIView,
    HistoriesFeedAPIView,
    CommentsListCreateAPIView,
    CommentsDestroyAPIView,
    TagListAPIView,
)

router = SimpleRouter(trailing_slash=False)
router.register(r"histories", HistoryViewSet, basename="histories")
router.register(r"tags", TagListAPIView, basename="tags")

urlpatterns = [
    path("api/", include(router.urls)),
    url(r"^histories/feed/?$", HistoriesFeedAPIView.as_view()),
    url(
        r"^histories/(?P<history_slug>[-\w]+)/favorite/?$",
        HistoriesFavoriteAPIView.as_view(),
    ),
    url(
        r"^histories/(?P<history_slug>[-\w]+)/comments/?$",
        CommentsListCreateAPIView.as_view(),
    ),
    url(
        r"^histories/(?P<history_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$",
        CommentsDestroyAPIView.as_view(),
    ),
]
