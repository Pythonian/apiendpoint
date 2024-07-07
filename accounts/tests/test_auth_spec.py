from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Organisation

User = get_user_model()


class TokenTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sapagrammer@hotmail.com",
            password="sapapassword",
            firstName="Seyi",
            lastName="Pythonian",
        )
        self.token = RefreshToken.for_user(self.user)

    def test_token_generation(self):
        # Check if the token contains the correct user ID
        self.assertEqual(self.token["userId"], str(self.user.userId))

        # Check if the token expires at the correct time
        expiration_time = self.token.access_token["exp"]
        expected_expiration_time = timezone.now() + timedelta(minutes=5)
        self.assertAlmostEqual(
            expiration_time,
            int(expected_expiration_time.timestamp()),
            delta=10,
        )


class OrganisationAccessTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="seyi@hotmail.com",
            password="password1",
            firstName="Seyi",
            lastName="Bello",
        )
        self.user2 = User.objects.create_user(
            email="sayo@hotmail.com",
            password="password2",
            firstName="Sayo",
            lastName="Bello",
        )
        self.org1 = Organisation.objects.create(name="Org1")
        self.org2 = Organisation.objects.create(name="Org2")
        self.org1.users.add(self.user1)
        self.org2.users.add(self.user2)

    def test_user_cannot_access_other_organisation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/organisations/{self.org2.orgId}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/organisations/{self.org1.orgId}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RegisterEndpointTestCase(APITestCase):
    def test_register_user_successfully(self):
        data = {
            "firstName": "Seyi",
            "lastName": "Bello",
            "email": "seyibello@hotmail.com",
            "password": "password123",
        }
        response = self.client.post("/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("accessToken", response.data["data"])
        self.assertEqual(
            response.data["data"]["user"]["email"],
            "seyibello@hotmail.com",
        )
        self.assertEqual(response.data["data"]["user"]["firstName"], "Seyi")
        self.assertEqual(response.data["data"]["user"]["lastName"], "Bello")

        user = User.objects.get(email="seyibello@hotmail.com")
        self.assertTrue(
            user.organisations.filter(name="Seyi's Organisation").exists(),
        )


class LoginEndpointTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sapagrammer@hotmail.com",
            password="sapapassword",
            firstName="Seyi",
            lastName="Pythonian",
        )

    def test_login_user_successfully(self):
        data = {"email": "sapagrammer@hotmail.com", "password": "sapapassword"}
        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("accessToken", response.data["data"])
        self.assertEqual(
            response.data["data"]["user"]["email"], "sapagrammer@hotmail.com"
        )

    def test_login_user_unsuccessfully(self):
        data = {"email": "sapagrammer@hotmail.com", "password": "wrongpass"}
        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterValidationTestCase(APITestCase):
    def test_missing_required_fields(self):
        data = {"firstName": "", "lastName": "", "email": "", "password": ""}
        response = self.client.post("/auth/register/", data)
        self.assertEqual(
            response.status_code,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
        self.assertIn(
            "firstName", [error["field"] for error in response.data["errors"]]
        )
        self.assertIn(
            "lastName",
            [error["field"] for error in response.data["errors"]],
        )
        self.assertIn(
            "email",
            [error["field"] for error in response.data["errors"]],
        )
        self.assertIn(
            "password",
            [error["field"] for error in response.data["errors"]],
        )


class DuplicateEmailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="madabevel@hotmail.com",
            password="password123",
            firstName="Vivian",
            lastName="Bello",
        )

    def test_duplicate_email_registration(self):
        data = {
            "firstName": "Ihuoma",
            "lastName": "Bello",
            "email": "madabevel@hotmail.com",
            "password": "password123",
        }
        response = self.client.post("/auth/register/", data)
        self.assertEqual(
            response.status_code,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
        self.assertIn(
            "email",
            [error["field"] for error in response.data["errors"]],
        )


class AddUserToOrganisationTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="seyi@hotmal.com",
            password="password1",
            firstName="Seyi",
            lastName="Bello",
        )
        self.user2 = User.objects.create_user(
            email="sayo@hotmal.com",
            password="password2",
            firstName="Sayo",
            lastName="Bello",
        )
        self.org = Organisation.objects.create(name="Test Organisation")

    def test_add_user_to_organisation_success(self):
        data = {"userId": str(self.user2.userId)}
        response = self.client.post(
            f"/api/organisations/{self.org.orgId}/users/",
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(
            response.data["message"], "User added to organisation successfully"
        )
        self.assertIn(self.user2, self.org.users.all())

    def test_add_user_to_organisation_user_not_found(self):
        data = {"userId": "58ec8b67-a05c-4608-8a20-3910b7953051"}
        response = self.client.post(
            f"/api/organisations/{self.org.orgId}/users/",
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"],
            "No User matches the given query.",
        )

    def test_add_user_to_organisation_organisation_not_found(self):
        data = {"userId": str(self.user2.userId)}
        response = self.client.post(
            "/api/organisations/58ec8b67-a05c-4608-8a20-3910b7953053/users/",
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Organisation matches the given query."
        )
