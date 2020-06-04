# from rest_framework.test import APITestCase, APIClient
# from rest_framework.authtoken.models import Token


# class BaseRestTestCase(APITestCase):
#     NUMBER_PAGES = 20

#     def setUp(self):
#         super().setUp()
#         token = Token.objects.get(user__username="lauren")
#         client = APIClient()
#         client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
