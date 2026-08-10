from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.


class CompanyTest(APITestCase):

    def setUp(self):

        self.registration_data = {
            "username": "owner-123",
            "email": "owner-123@google.com",
            "password": "owner-pass-123",
        }

        self.register_response = self.client.post(
            "/api/auth/register/",
            self.registration_data,
            format="json",
        )

        login = self.client.post(
            "/api/auth/token/",
            {
                "username": "owner-123",
                "password": "owner-pass-123",
            },
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data["access"]}")

    def test_authenticated_user_can_create_a_company(self):

        response = self.client.post(
            "/api/companies/",
            {
                "name": "nano Programming Inc.",
                "slug": "nano-programming-inc",
                "description": "This is a programming company that has a close relation with nano tech.",
            },
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {""}")

        response2 = self.client.post(
            "/api/companies/",
            {
                "name": "Real estate Programming Inc.",
                "slug": "real-estate-programming-inc",
                "description": "This is a programming company that has a close relation with real estate.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 401)

    def test_user_can_see_update_delete_his_company(self):

        self.client.post(
            "/api/companies/",
            {
                "name": "nano Programming Inc.",
                "slug": "nano-programming-inc",
                "description": "This is a programming company that has a close relation with nano tech.",
            },
            format="json",
        )

        response = self.client.get("/api/companies/me/")
        response2 = self.client.patch(
            "/api/companies/me/",
            {"name": "Boring company"},
            format="json",
        )
        response3 = self.client.delete("/api/companies/me/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 204)
