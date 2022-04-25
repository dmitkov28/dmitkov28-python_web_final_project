from django.contrib.auth import get_user_model
from django.test import TestCase

from python_web_final_project.accounts_app.forms import RegisterApplicantForm
from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.companies_app.models import CompanyProfile

UserModel = get_user_model()

class TestRegisterForm(TestCase):
    VALID_USER_DATA = {
        'email': 'user@mail.com',
        'password1': '123456qwe_!$',
        'password2': '123456qwe_!$',
    }

    def test_valid_form__expect_valid(self):
        form = RegisterApplicantForm(self.VALID_USER_DATA)
        self.assertTrue(form.is_valid())

    def test_valid_form_expect_correct_applicant_profile_created(self):
        form = RegisterApplicantForm(self.VALID_USER_DATA)
        form.save()
        user = UserModel.objects.first()
        profile = ApplicantProfile.objects.first()
        self.assertEqual(user, profile.user)
        self.assertFalse(user.is_company)

    def test_valid_form_is_company_expect_correct_company_profile_created(self):
        user_is_company = {'is_company': True}
        self.VALID_USER_DATA.update(user_is_company)
        form = RegisterApplicantForm(self.VALID_USER_DATA)
        form.save()
        profile = CompanyProfile.objects.first()
        user = UserModel.objects.first()
        self.assertTrue(form.is_valid())
        self.assertEqual(user, profile.user)
        self.assertTrue(user.is_company)



