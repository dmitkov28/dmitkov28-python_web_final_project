from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from python_web_final_project.accounts_app.forms import RegisterCompanyForm
from python_web_final_project.companies_app.models import CompanyProfile
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin

UserModel = get_user_model()


class TestRegisterCompanyView(TestCase, CreateUserAndProfileMixin):

    def test_correct_template_is_shown(self):
        self.client.get(reverse('register company'))
        self.assertTemplateUsed('accounts/register-company.html')

    def test_correct_forms_is_shown(self):
        response = self.client.get(reverse('register company'))
        form_shown = response.context['form']
        self.assertIsInstance(form_shown, RegisterCompanyForm)

    def test_authenticated_user_tries_to_register_as_company_expect_redirect_to_home(self):
        self._create_user()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('register company'))
        self.assertRedirects(response, reverse('index'))

    def test_valid_form_expect_correct_user_and_profile_to_be_created(self):
        self.client.post(reverse('register company'), data=self.VALID_COMPANY_REGISTER_DATA)
        user = UserModel.objects.first()
        company_profile = CompanyProfile.objects.first()
        self.assertTrue(user.is_company)
        self.assertEqual(user.email, self.VALID_COMPANY_REGISTER_DATA['email'])
        self.assertEqual(self.VALID_COMPANY_REGISTER_DATA['company_name'], company_profile.name)
        self.assertEqual(company_profile.user, user)

    def test_valid_form_expect_to_log_in_user_and_redirect_to_home(self):
        response = self.client.post(reverse('register company'), data=self.VALID_COMPANY_REGISTER_DATA)
        self.assertRedirects(response, reverse('index'))
        user = UserModel.objects.first()
        self.assertTrue(user.is_authenticated)

    def test_invalid_form_expect_user_not_to_be_created(self):
        self.client.post(reverse('register company'), data=self.INVALID_COMPANY_REGISTER_DATA)
        self.assertEqual(0, UserModel.objects.count())
        self.assertEqual(0, CompanyProfile.objects.count())
