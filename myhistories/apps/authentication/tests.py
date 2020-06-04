from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from myhistories.apps.authentication.models import User
from myhistories.apps.authentication.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)


class RegistrationAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("registration-list")

    def test_create_registration(self):
        users_count = User.objects.count()
        response = self.client.post(
            self.url,
            {
                "email": "juan@nieves.com",
                "password": "you_know_nothing",
                "is_active": "True",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), (users_count + 1))
        self.assertEqual(User.objects.last().email, "juan@nieves.com")

    # def test_list_users(self):
    #     """
    #     Test to verify user user list
    #     """

    #     response = self.client.get(self.url, limit=self.NUMBER_PAGES)
    #     self.assertEqual(
    #         response.json().get("count"), User.objects.count(),
    #     )


# class UserListCreateAPIViewTestCase(APITestCase):
#     def setUp(self):
#         super().setUp()
#         self.url = reverse("core:user-list")

#     def test_create_user(self):
#         users_count = User.objects.count()
#         response = self.client.post(
#             self.url,
#             {
#                 "email": "juan@nieves.com",
#                 "password": "you_know_nothing",
#                 "is_active": "True",
#             },
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), (users_count + 1))
#         self.assertEqual(User.objects.last().email, "juan@nieves.com")

#     def test_list_users(self):
#         """
#         Test to verify user user list
#         """

#         response = self.client.get(self.url, limit=self.NUMBER_PAGES)
#         self.assertEqual(
#             response.json().get("count"), User.objects.count(),
#         )


# class UserDetailAPIViewTestCase(APITestCase):
#     def setUp(self):
#         super().setUp()
#         with schema_context(schema_name=get_public_schema_name()):
#             self.user_test = User.objects.create_user(
#                 email="email@email.de", password="password1", is_active=True,
#             )
#         self.url = reverse("core:user-detail", kwargs={"pk": self.user_test.pk})

#     def test_user_object_detail(self):
#         """
#         Test to verify user object detail
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(200, response.status_code)
#         user_serializer_data = UserSerializer(instance=self.user_test).data
#         self.assertEqual(user_serializer_data, response.json())

#     def test_user_object_update(self):
#         response = self.client.put(
#             self.url,
#             {
#                 "email": "self@email.cc",
#                 "password": "self.password",
#                 "is_active": "True",
#             },
#         )
#         user = User.objects.get(id=self.user_test.id)
#         self.assertEqual(response.json().get("email"), user.email)

#     def test_user_object_partial_update(self):
#         response = self.client.patch(self.url, {"email": "self@email.cc"},)
#         user = User.objects.get(id=self.user_test.id)
#         self.assertEqual(response.json().get("email"), user.email)

#     def test_user_object_delete(self):
#         with schema_context(schema_name=self.tenant):
#             response = self.client.delete(self.url)
#         self.assertEqual(204, response.status_code)
