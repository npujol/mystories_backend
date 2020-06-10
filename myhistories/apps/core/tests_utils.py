from rest_framework.test import APITestCase, APIClient
from ..profiles.models import Profile
from ..authentication.models import User


class BaseRestTestCase(APITestCase):
    NUMBER_PAGES = 20

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="jonsnow", email="jon@snow.com", password="You_know_nothing123"
        )
        self.profile = Profile.objects.create(user=self.user, bio="bio")

        client = APIClient()
        client.force_authenticate(user=self.user.email)
