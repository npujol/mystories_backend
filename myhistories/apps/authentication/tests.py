from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.forms.models import model_to_dict


from ..core.tests_utils import BaseRestTestCase
from ..profiles.models import Profile

from .models import User
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("authentication:registration")

    def test_registration(self):
        users_count = User.objects.count()
        response = self.client.post(
            self.url,
            {
                "email": "juan@nieves.com",
                "username": "juancito",
                "password": "You_know_nothing123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), (users_count + 1))
        self.assertEqual(User.objects.last().email, "juan@nieves.com")


class LoginTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("authentication:login")

    def test_login_with_email(self):
        response = self.client.post(
            self.url, {"email": self.user.email, "password": "You_know_nothing123",},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.new_user = User.objects.create_user(
            username="notjon", email="nojon@snow.com", password="You_know_nothing123"
        )
        self.url = reverse(
            "authentication:user-detail", kwargs={"username": self.new_user.username}
        )

    def test_user_object_detail(self):
        """
        Test to verify user object detail
        """
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )
        self.assertEqual(200, response.status_code)
        user_serializer_data = UserSerializer(instance=self.new_user).data
        self.assertEqual(
            user_serializer_data.get("email"), response.json().get("user").get("email")
        )

    def test_user_object_update(self):
        response = self.client.put(
            self.url,
            {
                "username": "notjon",
                "email": "nojon@snow.com",
                "password": "You_know_nothing13",
                "profile": model_to_dict(self.new_user.profile),
            },
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )
        user = User.objects.get(username=self.new_user.username)
        print(response.json())
        self.assertEqual(response.json().get("user").get("username"), user.username)

    def test_user_object_partial_update(self):
        response = self.client.patch(
            self.url,
            {"username": "notjon"},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )
        user = User.objects.get(id=self.new_user.id)
        self.assertEqual(response.json().get("user").get("username"), user.username)
