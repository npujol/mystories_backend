from django.conf.urls import url

from .views import ProfileRetrieveUpdateAPIView, ProfileFollowAPIView

app_name = "profiles"

urlpatterns = [
    url(
        r"^api/profiles/(?P<user__username>\w+)/?$",
        ProfileRetrieveUpdateAPIView.as_view(),
        name="profile_detail",
    ),
    url(
        r"^api/profiles/(?P<user__username>\w+)/follow/?$",
        ProfileFollowAPIView.as_view(),
        name="profile_follow",
    ),
]
