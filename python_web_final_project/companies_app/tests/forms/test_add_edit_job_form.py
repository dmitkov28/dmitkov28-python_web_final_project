from django.test import TestCase

from python_web_final_project.companies_app.forms import CompanyAddEditJobForm
from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin


class TestAddEditJobForm(TestCase, CreateCompanyAndJobMixin):

    def setUp(self):
        self.company = self._create_company()

    def test_valid_data_expect_form_to_be_valid(self):
        form_data = {
            'role': 'Job Role',
            'company': self.company,
            'experience_level': 'Entry',
            'description': 'description',
            'work_schedule': 'Full-Time'
        }
        form = CompanyAddEditJobForm(company=self.company, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data_expect_form_to_be_invalid(self):
        form_data = {
            'role': '',
            'company': self.company,
            'experience_level': 'Entry',
            'description': 'description',
        }
        form = CompanyAddEditJobForm(company=self.company, data=form_data)
        self.assertFalse(form.is_valid())
