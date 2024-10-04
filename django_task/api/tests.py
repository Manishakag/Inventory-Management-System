import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse

from api.models import Item
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class TokenAuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.item = Item.objects.create(
            id=uuid.uuid4(),  # Use a UUID for the item ID
            name="Test Item",
            description="This is a test item.",
        )
        self.item_id = str(self.item.id)

    def test_token(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": "testuser", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_read_items_authenticated(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": "testuser", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = self.client.get(reverse("item-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_items_authenticated(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = self.client.post(
            reverse("create-item"),
            data={"name": "test", "description": "this is a test"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_items_authenticated(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        url = reverse("delete-item", args=[self.item_id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_items_authenticated(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        url = reverse("update-item", args=[self.item_id])
        response = self.client.put(
            url, data={"name": "test", "description": "test is a program"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
