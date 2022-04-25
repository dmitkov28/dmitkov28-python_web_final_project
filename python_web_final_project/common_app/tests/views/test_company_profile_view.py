from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateCompanyAndJobMixin


class TestCompanyProfileView(TestCase, CreateCompanyAndJobMixin):

    def test_correct_profile_when_profile_exists(self):
        company = self._create_company()
        profile = self._create_company_profile(company)
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('company profile', kwargs={'pk': company.pk}))
        self.assertEqual(profile, response.context_data['profile'])

    def test_when_profile_doesnt_exist_expect_404(self):
        company = self._create_company()
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('company profile', kwargs={'pk': company.pk}))
        self.assertEqual(404, response.status_code)

    def test_when_user_owns_profile_expect_can_edit(self):
        company = self._create_company()
        self._create_company_profile(company)
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('company profile', kwargs={'pk': company.pk}))
        print(response.context)
        self.assertTrue(response.context['can_edit'])

    def test_when_user_doesnt_own_profile_expect_can_edit_to_be_false(self):
        company2_credentials = {
            'email': 'company2@mail.com',
            'password': '654321ewq',
        }
        company = self._create_company()
        company_2 = self._create_company(**company2_credentials)
        self._create_company_profile(company)
        company_profile_2 = self._create_company_profile(company_2)

        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('company profile', kwargs={'pk': company_profile_2.pk}))
        self.assertFalse(response.context['can_edit'])
