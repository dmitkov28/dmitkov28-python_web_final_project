from django.contrib.auth import get_user_model
from django.test import TestCase

from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin

UserModel = get_user_model()


class ApplicantProfileTest(TestCase, CreateUserAndProfileMixin):

    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)

    def test_full_name_when_profile_has_first_and_last_name_expect_correct_full_name(self):
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.full_clean()
        self.profile.save()

        self.assertEqual(self.profile.full_name, 'Test User')
        self.assertEqual(self.profile.user, self.user)

    def test_full_name_when_only_first_name_expect_full_name_to_be_user_and_user_pk(self):
        self.profile.first_name = 'Test'
        self.profile.full_clean()
        self.profile.save()

        self.assertEqual(self.profile.full_name, f'User {self.user.pk}')



