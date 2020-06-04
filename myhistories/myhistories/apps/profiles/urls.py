from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

from .views import ProfileRetrieveAPIView, ProfileFollowAPIView

router = routers.SimpleRouter()
router.register(r"profileretrive", ProfileRetrieveAPIView, basename="profileretrive")
router.register(r"profilefollows", ProfileFollowAPIView, basename="profilefollows")

urlpatterns = [
    path("api/", include(router.urls)),
]
