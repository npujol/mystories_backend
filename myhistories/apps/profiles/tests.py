from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ..authentication.models import User
from ..core.tests_utils import BaseRestTestCase

from .models import Profile
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            "profiles:profile_retrieve", kwargs={"username": self.user.username}
        )

    def test_profile_object_detail(self):
        """
        Test to verify profile object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.tokens["access"]
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            ProfileSerializer(instance=self.profile).data,
            response.json().get("profile"),
        )


class ProfileFollowAPIView(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.user_test = User.objects.create_superuser(
            username="jonjon", email="jon@nosnow.com", password="You_know_nothing123"
        )
        self.profile_test = Profile.objects.create(
            user=self.user_test, bio="bio jonjon"
        )
        self.url = reverse(
            "profiles:profile_follow", kwargs={"username": self.user_test.username}
        )

    def test_unfollow_profile(self):
        """
        Test to verify unfollow profile
        """
        response = self.client.delete(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.tokens["access"]
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            ProfileSerializer(instance=self.profile_test).data,
            response.json().get("profile"),
        )
