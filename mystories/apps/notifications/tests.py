from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status

from ..core.tests_utils import BaseRestTestCase
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListCreateAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("notifications:notification-list")

    def test_create_history(self):
        notifications_count = Notification.objects.all().count()

        response = self.client.post(
            self.url,
            {
                "title": "string",
                "body": "string for the body",
                "receiver": model_to_dict(self.user.profile),
            },
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.all().count(), (notifications_count + 1))
        self.assertEqual(Notification.objects.last().title, "string")

    def test_list_histories(self):
        """
        Test to verify notifications list
        """
        response = self.client.get(
            self.url,
            limit=self.NUMBER_PAGES,
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        self.assertEqual(
            response.json().get("count"), Notification.objects.all().count()
        )


class NotificationDetailAPIViewTestCase(BaseRestTestCase):
    def setUp(self):
        super().setUp()
        self.notification = Notification.objects.create(
            author=self.user.profile,
            title="test",
            body="body for test",
            receiver=self.user.profile,
        )
        self.url = reverse(
            "notifications:notification-detail", kwargs={"pk": self.notification.pk}
        )

    def test_history_object_detail(self):
        """
        Test to verify a notification object detail
        """
        response = self.client.get(
            path=self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            NotificationSerializer(instance=self.notification).data["pk"],
            response.json().get("pk"),
        )

    def test_history_object_update(self):
        response = self.client.put(
            self.url,
            {
                "title": "string",
                "body": "string for the body",
                "receiver": model_to_dict(self.user.profile),
            },
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        notification = Notification.objects.get(id=self.notification.id)
        self.assertEqual(response.json().get("title"), notification.title)

    def test_history_object_partial_update(self):
        response = self.client.patch(
            self.url,
            {"body": "another body"},
            HTTP_AUTHORIZATION="Bearer " + self.user.token,
        )

        notification = Notification.objects.get(id=self.notification.id)
        self.assertEqual(response.json().get("body"), notification.body)

    def test_history_object_delete(self):
        response = self.client.delete(
            self.url, HTTP_AUTHORIZATION="Bearer " + self.user.token
        )

        self.assertEqual(204, response.status_code)
