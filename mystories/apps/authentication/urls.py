from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "authentication"
router = DefaultRouter(trailing_slash=False)
router.register("users", views.UserRetrieveUpdateAPIView, basename="user_detail")
router.register("auth/login", views.LoginAPIView, basename="login")
router.register("auth/registration", views.RegistrationAPIView, basename="registration")


urlpatterns = [path("", include(router.urls))]
