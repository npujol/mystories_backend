from rest_framework.test import APITestCase, APIClient
from ..authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class BaseRestTestCase(APITestCase):
    NUMBER_PAGES = 20

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="jonsnow", email="jon@snow.com", password="You_know_nothing123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        client = APIClient()
        client.credentials(token=self.tokens["access"])
