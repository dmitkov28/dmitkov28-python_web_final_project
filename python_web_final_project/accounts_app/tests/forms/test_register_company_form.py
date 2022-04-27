from django.contrib.auth import get_user_model
from django.test import TestCase

from python_web_final_project.accounts_app.forms import RegisterCompanyForm
from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.companies_app.models import CompanyProfile
from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin, CreateUserAndProfileMixin

UserModel = get_user_model()


class TestCompanyRegisterForm(TestCase, CreateUserAndProfileMixin, CreateCompanyAndJobMixin):

    def test_form_with_valid_data_expect_form_to_be_valid(self):
        form = RegisterCompanyForm(data=self.VALID_COMPANY_REGISTER_DATA)
        self.assertTrue(form.is_valid())

    def test_form_with_valid_data_expect_correct_profile_and_user_to_be_created(self):
        form = RegisterCompanyForm(data=self.VALID_COMPANY_REGISTER_DATA)
        form.save()
        user = UserModel.objects.first()
        company = CompanyProfile.objects.first()
        self.assertTrue(UserModel.objects.filter(email=self.VALID_COMPANY_REGISTER_DATA['email']))
        self.assertEqual(user.email, self.VALID_COMPANY_REGISTER_DATA['email'])
        self.assertTrue(user.is_company)
        self.assertEqual(0, ApplicantProfile.objects.count())
        self.assertTrue(CompanyProfile.objects.filter(user=user).exists())
        self.assertEqual(company.name, self.VALID_COMPANY_REGISTER_DATA['company_name'])

    def test_form_with_existing_company_name_expect_form_to_be_invalid(self):
        expected_error = RegisterCompanyForm.COMPANY_EXISTS_MESSAGE

        form = RegisterCompanyForm(data=self.VALID_COMPANY_REGISTER_DATA)
        form.save()

        form = RegisterCompanyForm(data=self.VALID_COMPANY_REGISTER_DATA)
        self.assertFalse(form.is_valid())
        self.assertTrue(expected_error in list(form.errors.values())[0])
        self.assertEqual(1, UserModel.objects.count())
        self.assertEqual(1, CompanyProfile.objects.count())
