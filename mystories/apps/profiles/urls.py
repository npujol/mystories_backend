from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProfileRetrieveUpdateAPIView

app_name = "profiles"
router = DefaultRouter(trailing_slash=False)
router.register("profiles", ProfileRetrieveUpdateAPIView, basename="profile_detail")

urlpatterns = [path("", include(router.urls))]
