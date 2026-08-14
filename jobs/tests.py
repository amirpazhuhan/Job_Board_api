from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Job, SavedJob
from companies.models import Company

# Create your tests here.


class JobsTest(APITestCase):

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
        self.user = get_user_model().objects.get(username="owner-123")

        self.company = Company.objects.create(
            owner=self.user,
            name="Test Company",
            slug="test-company",
            description="Test company",
        )
        self.job = Job.objects.create(
            company=self.company,
            title="Backend Developer",
            description="Build backend APIs.",
            salary_min=5000,
            salary_max=7000,
        )

    def test_authenticated_user_can_create_job(self):
        response = self.client.post(
            "/api/jobs/create/",
            {
                "title": "Janitor",
                "description": "Janitor cleans the environment around workplace.",
                "salary_min": 5000,
                "salary_max": 5500,
            },
            format="json",
        )
        response2 = self.client.post(
            "/api/jobs/create/",
            {
                "title": "Janitor",
                "description": "Janitor cleans the environment around workplace.",
                "company": 9999999,
                "salary_min": 5000,
                "salary_max": 5500,
            },
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer ")
        response3 = self.client.post(
            "/api/jobs/create/",
            {
                "title": "Janitor",
                "description": "Janitor cleans the environment around workplace.",
                "salary_min": 5000,
                "salary_max": 5500,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        job = Job.objects.get(id=response2.data["id"])
        self.assertEqual(job.company, self.user.company)
        self.assertEqual(response3.status_code, 401)

    def test_company_user_can_modify_delete_jobs(self):

        created_job = self.client.post(
            "/api/jobs/create/",
            {
                "title": "Janitor",
                "description": "Janitor cleans the environment around workplace.",
                "salary_min": 5000,
                "salary_max": 5500,
            },
            format="json",
        )
        id = created_job.data["id"]
        response = self.client.patch(
            f"/api/jobs/{id}/",
            {
                "title": "Janitor",
                "description": "Janitor cleans the environment around workplace.",
                "salary_min": 4000,
                "salary_max": 5000,
            },
            format="json",
        )
        response2 = self.client.get(f"/api/jobs/{id}/")
        response3 = self.client.delete(f"/api/jobs/{id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 204)
        self.assertFalse(Job.objects.filter(pk=1).exists())

    def test_authenticated_user_can_save_job(self):
        response = self.client.post(
            f"/api/jobs/{self.job.id}/save/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            SavedJob.objects.filter(
                user=self.user,
                job=self.job,
            ).exists()
        )

    def test_user_cannot_save_same_job_twice(self):
        SavedJob.objects.create(
            user=self.user,
            job=self.job,
        )

        response = self.client.post(
            f"/api/jobs/{self.job.id}/save/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            SavedJob.objects.filter(
                user=self.user,
                job=self.job,
            ).count(),
            1,
        )

    def test_authenticated_user_can_unsave_job(self):
        SavedJob.objects.create(
            user=self.user,
            job=self.job,
        )

        response = self.client.delete(
            f"/api/jobs/{self.job.id}/save/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            SavedJob.objects.filter(
                user=self.user,
                job=self.job,
            ).exists()
        )

    def test_user_cannot_unsave_another_users_job(self):
        other_user = get_user_model().objects.create_user(
            username="other-123",
            email="other-123@google.com",
            password="other-pass-123",
        )

        SavedJob.objects.create(
            user=other_user,
            job=self.job,
        )

        response = self.client.delete(
            f"/api/jobs/{self.job.id}/save/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            SavedJob.objects.filter(
                user=other_user,
                job=self.job,
            ).exists()
        )

    def test_user_can_list_saved_jobs(self):
        second_job = Job.objects.create(
            company=self.company,
            title="Django Developer",
            description="Build Django applications.",
            salary_min=6000,
            salary_max=8000,
        )

        SavedJob.objects.create(
            user=self.user,
            job=self.job,
        )

        SavedJob.objects.create(
            user=self.user,
            job=second_job,
        )

        response = self.client.get("/api/jobs/saved/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 2)
