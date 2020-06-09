from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import User
from ..core.tests_utils import BaseRestTestCase
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
        self.url = reverse("authentication:user-detail", kwargs={"pk": self.user.pk})

    def test_user_object_detail(self):
        """
        Test to verify user object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.tokens["access"]
        )
        self.assertEqual(200, response.status_code)
        user_serializer_data = UserSerializer(instance=self.user).data
        self.assertEqual(user_serializer_data, response.json().get("user"))

    def test_user_object_update(self):
        response = self.client.put(
            self.url,
            {
                "username": "another",
                "email": "jon@snow.com",
                "password": "You_know_nothing123",
                "profile": self.profile.id,
            },
            HTTP_AUTHORIZATION="Bearer " + self.tokens["access"],
        )
        user = User.objects.get(id=self.user.id)
        self.assertEqual(response.json().get("user").get("username"), user.username)

    def test_user_object_partial_update(self):
        response = self.client.patch(
            self.url,
            {"username": "another"},
            HTTP_AUTHORIZATION="Bearer " + self.tokens["access"],
        )
        user = User.objects.get(id=self.user.id)
        self.assertEqual(response.json().get("user").get("username"), user.username)
