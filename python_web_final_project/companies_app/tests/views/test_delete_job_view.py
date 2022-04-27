from django.test import TestCase
from django.urls import reverse

from python_web_final_project.common_app.models import Job
from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin, CreateUserAndProfileMixin

class TestDeleteJobView(TestCase, CreateCompanyAndJobMixin, CreateUserAndProfileMixin):

    company2_credentials = {
        'email': 'company2@email.com',
        'password': '123456qwe'
    }

    def setUp(self):
        self.company = self._create_company()
        self.company_profile = self._create_company_profile(self.company)
        self.company_2 = self._create_company(**self.company2_credentials)
        self.job = self._create_job(self.company)

    def test_delete_job_when_user_is_owner_expect_job_to_be_deleted(self):
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        self.client.post(reverse('delete job', kwargs={'pk': self.job.pk}))
        self.assertEqual(0, len(Job.objects.filter(company=self.company)))

    def test_delete_job_when_user_is_owner_expect_redirect_to_company_jobs(self):
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.post(reverse('delete job', kwargs={'pk': self.job.pk}))
        self.assertRedirects(response, reverse('company jobs', kwargs={'pk': self.company.pk}))

    def test_delete_job_when_user_is_not_owner_expect_job_not_to_be_deleted(self):
        self.client.login(**self.company2_credentials)
        self.client.post(reverse('delete job', kwargs={'pk': self.job.pk}))
        self.assertIn(self.job, Job.objects.all())

    def test_delete_job_when_user_is_not_owner_expect_redirect_to_job_details_page(self):
        self.client.login(**self.company2_credentials)
        response = self.client.post(reverse('delete job', kwargs={'pk': self.job.pk}))
        self.assertRedirects(response, reverse('job details', kwargs={'pk': self.job.pk}))
