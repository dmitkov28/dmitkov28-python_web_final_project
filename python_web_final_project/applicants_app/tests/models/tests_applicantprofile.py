from django.contrib.auth import get_user_model
from django.test import TestCase

from python_web_final_project.applicants_app.models.main_models import ApplicantProfile

UserModel = get_user_model()


class ApplicantProfileTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser@mail.com',
        'password': '12345qew',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'current_occupation': 'Python Developer',
        'address': 'Sofia, Bulgaria',

    }

    def _create_valid_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def test_full_name_when_valid_expect_correct_full_name(self):
        user = self._create_valid_user(**self.VALID_USER_CREDENTIALS)
        profile = ApplicantProfile(
            **self.VALID_PROFILE_DATA,
            user=user)
        profile.full_clean()
        profile.save()
        expected_full_name = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertCountEqual(expected_full_name, profile.full_name)
