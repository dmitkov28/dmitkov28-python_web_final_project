from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin

UserModel = get_user_model()

class TestCustomUserModel(TestCase, CreateUserAndProfileMixin):

    def test_create_user_with_valid_credentials_expect_correct_user_to_be_created(self):
        user = UserModel(**self.VALID_USER_CREDENTIALS)
        user.full_clean()
        user.save()
        self.assertEqual(user, UserModel.objects.first())
        self.assertFalse(user.is_company)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_with_invalid_credentials_expect_validation_error(self):
        INVALID_USER_CREDENTIALS = {
            'email': 'abcd',
            'password': '123456qwe',
        }

        user = UserModel(**INVALID_USER_CREDENTIALS)
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_create_user_with_existing_email_expect_validation_error(self):
        user = UserModel(**self.VALID_USER_CREDENTIALS)
        user.full_clean()
        user.save()

        user2 = UserModel(**self.VALID_USER_CREDENTIALS)
        with self.assertRaises(ValidationError):
            user2.full_clean()


