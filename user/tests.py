from rest_framework.test import APITestCase

# Create your tests here.


class AuthenticationAPItests(APITestCase):

    def setUp(self):
        self.registration_data = {
            "username": "applicant-123",
            "email": "applicant@google.com",
            "password": "applicant-pass-123",
        }

        self.register_response = self.client.post(
            "/api/auth/register/",
            self.registration_data,
            format="json",
        )

    def test_user_registered_successfully(self):

        self.assertEqual(self.register_response.status_code, 201)

    def test_user_login_returns_access_refresh_token(self):

        response = self.client.post(
            "/api/auth/token/",
            {
                "username": "applicant-123",
                "password": "applicant-pass-123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_can_read_update_their_own_profile(self):

        login = self.client.post(
            "/api/auth/token/",
            {
                "username": "applicant-123",
                "password": "applicant-pass-123",
            },
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data["access"]}")

        response = self.client.patch(
            "/api/auth/profile/", {"phone_number": "123456789"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["phone_number"], "123456789")

    def test_user_can_change_his_password(self):

        login = self.client.post(
            "/api/auth/token/",
            {
                "username": "applicant-123",
                "password": "applicant-pass-123",
            },
            format="json",
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data["access"]}")

        response = self.client.patch(
            "/api/auth/change_password/",
            {
                "old_password": "applicant-pass-123",
                "new_password": "applicant-pass-4567",
            },
            format="json",
        )
        response2 = self.client.patch(
            "/api/auth/change_password/",
            {"old_password": "applicant-pass-123", "new_password": ""},
            format="json",
        )
        response3 = self.client.patch(
            "/api/auth/change_password/",
            {
                "old_password": "applicant-pass123",
                "new_password": "applicant-pass-4567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(response2.status_code, 400)
