from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin


class TestCompanyEditJobView(TestCase, CreateCompanyAndJobMixin):
    INVALID_JOB_PK = 100

    def setUp(self):
        self.company = self._create_company()
        self.company_profile = self._create_company_profile(self.company)
        self.job = self._create_job(self.company)
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)

    def test_correct_form_action_in_context(self):
        expected_form_action = 'Edit Job'
        response = self.client.get(reverse('edit job', kwargs={'pk': self.job.pk}))
        self.assertEqual(response.context['form_action'], expected_form_action)

    def test_non_existing_job_expect_404(self):
        response = self.client.get(reverse('edit job', kwargs={'pk': self.INVALID_JOB_PK}))
        self.assertEqual(404, response.status_code)

