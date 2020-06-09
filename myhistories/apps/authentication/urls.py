from django.conf.urls import url
from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView


app_name = "authentication"
urlpatterns = [
    url(
        r"^users/(?P<pk>[0-9]+)/$",
        UserRetrieveUpdateAPIView.as_view(),
        name="user-detail",
    ),
    url(r"^api/registration$", RegistrationAPIView.as_view(), name="registration"),
    url(r"^api/login$", LoginAPIView.as_view(), name="login"),
]
