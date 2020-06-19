from django.conf import settings
from rest_framework.test import APIClient, APITestCase

from ..authentication.models import User
from ..profiles.models import Profile


class BaseRestTestCase(APITestCase):
    settings.CELERY_ALWAYS_EAGER = True
    NUMBER_PAGES = 20

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="jonsnow", email="jon@snow.com", password="You_know_nothing123"
        )
        client = APIClient()
        client.force_authenticate(user=self.user.email)
