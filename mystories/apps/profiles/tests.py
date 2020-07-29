from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..authentication.models import User
from ..core.tests_utils import BaseRestTestCase
from .models import Profile
from .serializers import ProfileSerializer


class ProfileAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.user_test = User.objects.create_superuser(
            username="jonjon", email="jon@nosnow.com", password="You_know_nothing123"
        )
        self.url = reverse(
            "profiles:profile-detail", kwargs={"user__username": self.user.username}
        )

    def test_profile_object_detail(self):
        """
        Test to verify profile object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )
        self.assertEqual(200, response.status_code)

    def test_profile_object_update(self):
        response = self.client.put(
            self.url,
            {"bio": "another bio", "image": "image"},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(response.json().get("bio"), profile.bio)

    def test_profile_object_partial_update(self):
        response = self.client.patch(
            self.url,
            {"bio": "another more"},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )
        profile = Profile.objects.get(id=self.user.profile.id)
        self.assertEqual(response.json().get("username"), profile.user.username)

    def test_follow_profile(self):
        """
        Test to verify follow profile
        """
        url = reverse(
            "profiles:profile-follow_profile",
            kwargs={"user__username": self.user_test.username},
        )
        response = self.client.post(url, HTTP_AUTHORIZATION="Bearer " + self.user.token)
        print(response.json())
        self.assertEqual(201, response.status_code)
        self.assertTrue(response.json()["following"])

    def test_unfollow_profile(self):
        """
        Test to verify unfollow profile
        """
        url = reverse(
            "profiles:profile-unfollow_profile",
            kwargs={"user__username": self.user_test.username},
        )
        response = self.client.delete(
            url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.json()["following"])
