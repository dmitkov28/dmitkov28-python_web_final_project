from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin, CreateUserAndProfileMixin


class TestJobDetailsView(TestCase, CreateCompanyAndJobMixin, CreateUserAndProfileMixin):
    NON_EXISTING_JOB_PK = 100
    COMPANY_2_CREDENTIALS = {
        'email': 'company2@mail.com',
        'password': '123456qwe',
    }

    def test_get_non_existing_job_expect_404(self):
        response = self.client.get(reverse('job details', kwargs={'pk': self.NON_EXISTING_JOB_PK}))
        self.assertEqual(404, response.status_code)

    def test_existing_job_expect_correct_result(self):
        company = self._create_company()
        self._create_company_profile(company)
        job = self._create_job(company)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(job, response.context_data['job'])

    def test_logged_in_user_expect_can_apply(self):
        self._create_user()
        company = self._create_company()
        self._create_company_profile(company)
        job = self._create_job(company)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertTrue(response.context['can_apply'])

    def test_user_not_logged_in_expect_can_apply_to_be_false(self):
        company = self._create_company()
        self._create_company_profile(company)
        job = self._create_job(company)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertFalse(response.context['can_apply'])

    def test_user_is_company_expect_can_apply_to_be_false(self):
        company = self._create_company()
        self._create_company_profile(company)
        job = self._create_job(company)
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertFalse(response.context['can_apply'])

    def test_user_is_company_that_created_job_expect_can_edit_to_be_true(self):
        company = self._create_company()
        self._create_company_profile(company)
        job = self._create_job(company)
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertTrue(response.context['can_edit'])

    def test_user_is_different_company_expect_can_edit_to_be_false(self):
        company = self._create_company()
        self._create_company_profile(company)
        job = self._create_job(company)
        self._create_company(**self.COMPANY_2_CREDENTIALS)
        self.client.login(**self.COMPANY_2_CREDENTIALS)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertFalse(response.context['can_edit'])
