from django.core.exceptions import ValidationError
from django.test import TestCase

from python_web_final_project.applicants_app.models.main_models import TechnicalSkill
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin


class TestTechnicalSkill(TestCase, CreateUserAndProfileMixin):

    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)

    def test_valid_skill_expect_correct_skill_to_be_created(self):
        user = self.user
        skill = TechnicalSkill(
            name='Python',
            level=65,
            user=user,
        )
        skill.full_clean()
        skill.save()
        self.assertEqual(skill, self.user.technicalskill_set.first())

    def test_skill_level_gt100_expect_validation_error(self):
        user = self.user
        skill = TechnicalSkill(
            name='Python',
            level=1000,
            user=user,
        )

        with self.assertRaises(ValidationError):
            skill.full_clean()

    def test_skill_level_lt_0_expect_validation_error(self):
        user = self.user
        skill = TechnicalSkill(
            name='Python',
            level=-10,
            user=user,
        )

        with self.assertRaises(ValidationError):
            skill.full_clean()
