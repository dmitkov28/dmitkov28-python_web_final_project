from django.contrib.auth import get_user_model
from django.test import TestCase

from python_web_final_project.accounts_app.forms import RegisterApplicantForm
from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin

UserModel = get_user_model()


class TestRegisterApplicantForm(TestCase, CreateUserAndProfileMixin):
    VALID_REGISTER_FORM_DATA = {
        'email': 'user@mail.com',
        'password1': '123456qwe_!$',
        'password2': '123456qwe_!$',
    }

    def test_form_with_valid_data_expect_form_to_be_valid(self):
        form = RegisterApplicantForm(data=self.VALID_REGISTER_FORM_DATA)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data_expect_form_to_be_invalid(self):
        form = RegisterApplicantForm(data={'email': 'invalid', 'password1': 'invalid', 'password2': 'invalid'})
        self.assertFalse(form.is_valid())

    def test_form_with_existing_user_expect_form_to_be_invalid(self):
        expected_error_message = 'User with this Email already exists.'
        user = self._create_user()
        self._create_profile(user)
        form = RegisterApplicantForm(data=
                                     {'email': self.VALID_USER_CREDENTIALS['email'],
                                      'password1': self.VALID_REGISTER_FORM_DATA['password1'],
                                      'password2': self.VALID_REGISTER_FORM_DATA['password1'],
                                      })

        self.assertFalse(form.is_valid())
        self.assertTrue(expected_error_message in form.errors['email'])
        self.assertEqual(1, ApplicantProfile.objects.count())
        self.assertEqual(user.pk, ApplicantProfile.objects.first().pk)


    def test_form_with_valid_data_expect_correct_user_and_profile_to_be_created(self):
        form = RegisterApplicantForm(data=self.VALID_REGISTER_FORM_DATA)
        form.save()
        user = UserModel.objects.first()
        self.assertTrue(1, UserModel.objects.count())
        self.assertEqual(user.email, self.VALID_REGISTER_FORM_DATA['email'])
        self.assertTrue(ApplicantProfile.objects.filter(user=user).exists())
        self.assertFalse(user.is_company)
        self.assertEqual(self.VALID_REGISTER_FORM_DATA['email'], user.email)
