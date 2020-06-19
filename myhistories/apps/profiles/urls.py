from django.urls import path

from .views import ProfileFollowAPIView, ProfileRetrieveUpdateAPIView

app_name = "profiles"

urlpatterns = [
    path(
        "profiles/<str:user__username>/",
        ProfileRetrieveUpdateAPIView.as_view(),
        name="profile_detail",
    ),
    path(
        "profiles/<str:user__username>/follow/",
        ProfileFollowAPIView.as_view(),
        name="profile_follow",
    ),
]
