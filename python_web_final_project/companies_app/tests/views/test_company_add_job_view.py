from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin


class TestCompanyAddJobView(TestCase, CreateCompanyAndJobMixin):

    def setUp(self):
        self.company = self._create_company()
        self.company_profile = self._create_company_profile(self.company)
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)

    def test_correct_form_action_in_context(self):
        expected_form_action = 'Add Job'
        response = self.client.get(reverse('add job'))
        self.assertEqual(response.context['form_action'], expected_form_action)


