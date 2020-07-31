from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "profiles"
router = DefaultRouter(trailing_slash=False)
router.register("profiles", views.ProfileRetrieveUpdateAPIView, basename="profile")

urlpatterns = [path("", include(router.urls))]
