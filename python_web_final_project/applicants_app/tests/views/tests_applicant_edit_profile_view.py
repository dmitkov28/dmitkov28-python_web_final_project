from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from python_web_final_project.applicants_app.forms import ApplicantEditProfileForm
from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin

UserModel = get_user_model()


class TestApplicantEditProfileView(CreateUserAndProfileMixin, TestCase):

    def setUp(self):
        self.user = self._create_user()

    def test_logged_in_user_with_valid_profile_expect_status_200(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('edit applicant profile'))
        self.assertEqual(200, response.status_code)

    def test_user_not_logged_in_expect_redirect_to_login(self):
        response = self.client.get(reverse('edit applicant profile'))
        self.assertRedirects(response, reverse('index'))

    def test_correct_template_is_shown(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('edit applicant profile'))
        self.assertTemplateUsed(response, 'applicant_templates/edit-profile.html')

    def test_view_returns_correct_form(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('edit applicant profile'))
        self.assertIsInstance(response.context['form'], ApplicantEditProfileForm)

    def test_view_returns_correct_profile_object(self):
        profile = self._create_profile(self.user)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('edit applicant profile'))
        self.assertEqual(response.context_data['object'], profile)

    def test_view_updates_profile_correctly(self):
        self._create_profile(self.user)
        updated_profile_data = {
            'first_name': 'Updated',
            'last_name': 'Profile Name',
            'address': 'Address',
        }

        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.post(reverse('edit applicant profile'), data=updated_profile_data)

        profile = ApplicantProfile.objects.first()

        self.assertEqual('Updated', profile.first_name)
        self.assertEqual('Profile Name', profile.last_name)
        self.assertEqual('Address', profile.address)

    def test_view_redirects_on_success(self):
        profile = self._create_profile(self.user)
        profile.first_name = 'User'
        profile.full_clean()
        profile.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.get(reverse('edit applicant profile'))
        data = {
            'first_name': 'Updated First Name',
        }

        response = self.client.post(reverse('edit applicant profile'), data)
        self.assertRedirects(response, reverse('applicant profile', kwargs={'pk': self.user.pk}))





