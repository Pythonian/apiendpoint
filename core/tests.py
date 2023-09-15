from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Person


class PersonAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = reverse("create_user")

    def test_create_user_valid_data(self):
        data = {"name": "JohnDoe"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get().name, "JohnDoe")

    def test_create_user_invalid_data(self):
        data = {"name": 123}  # Invalid data with a number
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Person.objects.count(), 0)

    def test_get_user_valid_id(self):
        user = Person.objects.create(name="Pythonian")
        url = reverse("get_user", args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Pythonian")

    def test_get_user_invalid_id(self):
        url = reverse("get_user", args=[999])  # Non-existent user ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_valid_id(self):
        user = Person.objects.create(name="Pythonian")
        url = reverse("get_user", args=[user.id])
        updated_data = {"name": "NewName"}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Person.objects.get(id=user.id).name, "NewName")

    def test_update_user_invalid_id(self):
        url = reverse("get_user", args=[999])  # Non-existent user ID
        updated_data = {"name": "NewName"}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_valid_id(self):
        user = Person.objects.create(name="Pythonian")
        url = reverse("get_user", args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Person.objects.count(), 0)

    def test_delete_user_invalid_id(self):
        url = reverse("get_user", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_name_valid_name(self):
        user = Person.objects.create(name="Prontomaster")
        url = reverse("get_user_name", args=[user.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Prontomaster")

    def test_get_user_name_invalid_name(self):
        url = reverse("get_user_name", args=["NonExistentName"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user_duplicate_name(self):
        # Attempt to create a user with a name that already exists
        Person.objects.create(name="Pythonian")
        data = {"name": "Pythonian"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_same_name(self):
        # Attempt to update a user with the same name (no changes)
        user = Person.objects.create(name="Pythonian")
        url = reverse("get_user", args=[user.id])
        updated_data = {"name": "Pythonian"}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Person.objects.get(id=user.id).name, "Pythonian")

    def test_update_user_empty_name(self):
        user = Person.objects.create(name="Pythonian")
        url = reverse("get_user", args=[user.id])
        updated_data = {"name": ""}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_already_deleted(self):
        # Create a user
        user = Person.objects.create(name="John Doe")
        user_id = user.id

        # Delete the user
        user.delete()

        # Attempt to delete the user again
        url = reverse("get_user", args=[user_id])
        response = self.client.delete(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check that the response contains an error message
        self.assertEqual(response.data["error"], f"User with ID {user_id} not found")
