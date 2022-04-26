from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin

UserModel = get_user_model()

class TestRegisterCompanyView(TestCase, CreateUserAndProfileMixin):
    VALID_COMPANY_REGISTER_DATA = {
        'email': 'user@mail.com',
        'password1': '_qWe!@&#l>10pr_',
        'password2': '_qWe!@&#l>10pr_',
        'name': 'Company'
    }

    def test_correct_template(self):
        self.client.get(reverse('register company'))
        self.assertTemplateUsed('accounts/register-company.html')

    def test_authenticated_user_tries_to_register_expect_redirect_to_home(self):
        self._create_user()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('register applicant'))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('index'))

    def test_authenticated_user_tries_to_register_as_company_expect_redirect_to_home(self):
        self._create_user()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('register company'))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('index'))

    def test_valid_form_expect_to_log_in_user_and_redirect_to_home(self):
        response = self.client.post(reverse('register applicant'), data=self.VALID_COMPANY_REGISTER_DATA)
        self.assertRedirects(response, reverse('index'))
        user = UserModel.objects.first()
        self.assertTrue(user.is_authenticated)






