from django.contrib.auth import get_user_model
from django.test import TestCase

from python_web_final_project.applicants_app.models.main_models import TechnicalSkill

UserModel = get_user_model()


class TestTechnicalSkill(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser@mail.com',
        'password': '12345qew',
    }

    def _create_user(self, **credentials):
        return UserModel.objects.create(**credentials)

    def test_valid_skill_should_create_skill(self):
        user = self._create_user(**self.VALID_USER_CREDENTIALS)
        skill = TechnicalSkill(
            name='Python',
            level=65,
            user=user,
        )
        skill.full_clean()
        skill.save()
        self.assertIsNotNone(skill.pk)
