from django.test import TestCase
from django.urls import reverse

from python_web_final_project.common_app.models import Job
from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin, CreateUserAndProfileMixin


class TestCompanyJobsView(TestCase, CreateCompanyAndJobMixin, CreateUserAndProfileMixin):

    def setUp(self):
        self.company = self._create_company()
        self.company_profile = self._create_company_profile(self.company)

    def test_when_no_jobs_expect_empty_queryset(self):
        response = self.client.get(reverse('company jobs', kwargs={'pk': self.company.pk}))
        self.assertEqual(0, len(response.context['jobs']))

    def test_when_jobs_expect_correct_queryset(self):
        job = self._create_job(self.company)
        expected_queryset = Job.objects.filter(company=self.company).order_by('-date_added')
        response = self.client.get(reverse('company jobs', kwargs={'pk': self.company.pk}))
        self.assertQuerysetEqual(expected_queryset, response.context['jobs'])

    def test_when_user_owns_profile_expect_can_edit_to_be_true(self):
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('company jobs', kwargs={'pk': self.company.pk}))
        self.assertTrue(response.context['can_edit'])

    def test_when_user_does_not_own_profile_expect_can_edit_to_be_true(self):
        self._create_user()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('company jobs', kwargs={'pk': self.company.pk}))
        self.assertFalse(response.context['can_edit'])

    def test_when_user_not_authenticated_expect_can_edit_to_be_true(self):
        response = self.client.get(reverse('company jobs', kwargs={'pk': self.company.pk}))
        self.assertFalse(response.context['can_edit'])


