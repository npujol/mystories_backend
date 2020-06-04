from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers
from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

router = routers.SimpleRouter()
router.register(r"users", UserRetrieveUpdateAPIView, basename="user")
router.register(r"registations", RegistrationAPIView, basename="registation")


urlpatterns = [
    path("api/", include(router.urls)),
]
