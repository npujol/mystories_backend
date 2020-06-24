from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "notifications"

router = DefaultRouter(trailing_slash=False)
router.register("notifications", views.NotificationViewSet, basename="notification")


urlpatterns = [path("", include(router.urls))]
