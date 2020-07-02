from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

app_name = "authentication"

urlpatterns = [
    path("auth/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain"),
    path(
        "auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "users/<str:username>/", UserRetrieveUpdateAPIView.as_view(), name="user-detail"
    ),
    path("auth/registration/", RegistrationAPIView.as_view(), name="registration"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
]
