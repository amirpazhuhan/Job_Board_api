from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from applications.models import Application
from companies.models import Company
from jobs.models import Job

User = get_user_model()


class ApplicationTests(APITestCase):

    def setUp(self):
        # Users
        self.company_owner = User.objects.create_user(
            username="company_owner",
            email="owner@example.com",
            password="password123",
        )

        self.applicant = User.objects.create_user(
            username="applicant",
            email="applicant@example.com",
            password="password123",
        )

        self.other_applicant = User.objects.create_user(
            username="other_applicant",
            email="other_applicant@example.com",
            password="password123",
        )

        self.other_company_owner = User.objects.create_user(
            username="other_owner",
            email="other_owner@example.com",
            password="password123",
        )

        # Companies
        self.company = Company.objects.create(
            owner=self.company_owner,
            slug="company-a",
        )

        self.company_owner.company = self.company
        self.company_owner.save()

        self.other_company = Company.objects.create(
            owner=self.other_company_owner,
            slug="company-b",
        )

        self.other_company_owner.company = self.other_company
        self.other_company_owner.save()

        # Jobs
        self.job = Job.objects.create(
            company=self.company,
            title="Backend Developer",
            description="Django backend developer",
            salary_min=5000,
            salary_max=7000,
        )

        self.other_job = Job.objects.create(
            company=self.other_company,
            title="Frontend Developer",
            description="Frontend developer",
            salary_min=4000,
            salary_max=6000,
        )

    def make_resume(self):
        return SimpleUploadedFile(
            "resume.pdf",
            b"fake resume content",
            content_type="application/pdf",
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # -------------------------
    # Applying for a job
    # -------------------------

    def test_applicant_can_apply_for_job(self):
        self.authenticate(self.applicant)

        response = self.client.post(
            f"/api/applications/{self.job.id}/apply/",
            {
                "cover_letter": "I would like to apply.",
                "resume": self.make_resume(),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        application = Application.objects.get(
            job=self.job,
            user=self.applicant,
        )

        self.assertEqual(
            application.status,
            Application.Status.PENDING,
        )

        self.assertEqual(
            application.job,
            self.job,
        )

        self.assertEqual(
            application.user,
            self.applicant,
        )

    def test_applicant_cannot_apply_twice_to_same_job(self):
        Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="First application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.applicant)

        response = self.client.post(
            f"/api/applications/{self.job.id}/apply/",
            {
                "user": self.applicant,
                "cover_letter": "Second application",
                "resume": self.make_resume(),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # -------------------------
    # List applications
    # -------------------------

    def test_applicant_can_see_own_applications(self):

        application1 = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="Application 1",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        application2 = Application.objects.create(
            job=self.other_job,
            user=self.applicant,
            cover_letter="Application 2",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        # Belongs to another applicant.
        Application.objects.create(
            job=self.job,
            user=self.other_applicant,
            cover_letter="Other application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.applicant)

        response = self.client.get("/api/applications/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

        returned_ids = {application["id"] for application in response.data}

        self.assertEqual(
            returned_ids,
            {application1.id, application2.id},
        )

    def test_company_owner_can_see_applications_for_company_jobs(self):
        application1 = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="Application 1",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        # Belongs to another company.
        Application.objects.create(
            job=self.other_job,
            user=self.other_applicant,
            cover_letter="Application 2",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.company_owner)

        response = self.client.get("/api/applications/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            application1.id,
        )

    # -------------------------
    # Company application detail
    # -------------------------

    def test_company_owner_can_retrieve_company_application(self):
        application = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="Application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.company_owner)

        response = self.client.get(f"/api/applications/{application.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            application.id,
        )

    def test_company_owner_can_change_application_status(self):
        application = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="Application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.company_owner)

        response = self.client.patch(
            f"/api/applications/{application.id}/",
            {
                "status": Application.Status.ACCEPTED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        application.refresh_from_db()

        self.assertEqual(
            application.status,
            Application.Status.ACCEPTED,
        )

    def test_company_owner_cannot_access_other_company_application(self):
        application = Application.objects.create(
            job=self.other_job,
            user=self.other_applicant,
            cover_letter="Application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.company_owner)

        response = self.client.get(f"/api/applications/{application.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_company_owner_cannot_change_job_or_user(self):
        application = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="Application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.company_owner)

        response = self.client.patch(
            f"/api/applications/{application.id}/",
            {
                "job": self.other_job.id,
                "user": self.other_applicant.id,
                "status": Application.Status.REVIEWING,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        application.refresh_from_db()

        self.assertEqual(
            application.job,
            self.job,
        )

        self.assertEqual(
            application.user,
            self.applicant,
        )

        self.assertEqual(
            application.status,
            Application.Status.REVIEWING,
        )

    # -------------------------
    # Applicant application detail
    # -------------------------

    def test_applicant_can_see_own_application(self):
        application = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="My application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.applicant)

        response = self.client.get(f"/api/applications/my/{application.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            application.id,
        )

    def test_applicant_cannot_see_another_users_application(self):
        application = Application.objects.create(
            job=self.job,
            user=self.other_applicant,
            cover_letter="Other application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.applicant)

        response = self.client.get(f"/api/applications/my/{application.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_applicant_cannot_change_application_status(self):
        application = Application.objects.create(
            job=self.job,
            user=self.applicant,
            cover_letter="My application",
            resume=self.make_resume(),
            status=Application.Status.PENDING,
        )

        self.authenticate(self.applicant)

        response = self.client.patch(
            f"/api/applications/my/{application.id}/",
            {
                "status": Application.Status.ACCEPTED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        application.refresh_from_db()

        self.assertEqual(
            application.status,
            Application.Status.PENDING,
        )
