from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin
from python_web_final_project.helpers.mixins.view_mixins import CompanyAddEditJobViewMixin


class TestCompanyAddEditJobViewMixin(TestCase, CreateCompanyAndJobMixin):

    def setUp(self):
        self.company = self._create_company()
        self.company_profile = self._create_company_profile(self.company)
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)

    def test_view_returns_correct_template(self):
        response = self.client.get(reverse('add job'))
        expected_template = CompanyAddEditJobViewMixin.template_name
        self.assertTemplateUsed(response, expected_template)

    def test_view_returns_correct_form(self):
        response = self.client.get(reverse('add job'))
        expected_form_class = CompanyAddEditJobViewMixin.form_class
        self.assertIsInstance(response.context['form'], expected_form_class)

    def test_form_has_correct_company(self):
        response = self.client.get(reverse('add job'))
        self.assertEqual(self.company, response.context['form'].company)



