from django.test import TestCase

from python_web_final_project.applicants_app.forms import ApplicantEditTechnicalSkillsFormset
from python_web_final_project.applicants_app.models.main_models import TechnicalSkill
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, FormsetTestDataMixin


class TestEditSkills(TestCase, CreateUserAndProfileMixin, FormsetTestDataMixin):


    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)
        self.VALID_FORMSET_DATA = {
        'technicalskill_set-0-name': 'Django',
        'technicalskill_set-0-level': 60,
        'technicalskill_set-TOTAL_FORMS': '1',
        'technicalskill_set-INITIAL_FORMS': '0',
        'technicalskill_set-MIN_NUM_FORMS': '0',
        'technicalskill_set-MAX_NUM_FORMS': '1000',
    }

    def test_formset_with_valid_data_expect_formset_to_be_valid(self):
        formset = ApplicantEditTechnicalSkillsFormset(instance=self.user, data=self.VALID_FORMSET_DATA)
        self.assertTrue(formset.is_valid())


    def test_formset_with_valid_data_expect_correct_skill_to_be_created(self):
        formset = ApplicantEditTechnicalSkillsFormset(instance=self.user, data=self.VALID_FORMSET_DATA)
        if formset.is_valid():
            formset.save()
        skill = TechnicalSkill.objects.first()
        self.assertEqual(skill.name, self.VALID_FORMSET_DATA['technicalskill_set-0-name'])
        self.assertEqual(skill.level, self.VALID_FORMSET_DATA['technicalskill_set-0-level'])

    def test_formset_with_invalid_data_expect_formset_to_be_invalid_and_no_objects_to_be_created(self):
        self.VALID_FORMSET_DATA['technicalskill_set-0-level'] = 9000
        formset = ApplicantEditTechnicalSkillsFormset(instance=self.user, data=self.VALID_FORMSET_DATA)
        self.assertFalse(formset.is_valid())
        self.assertEqual(0, TechnicalSkill.objects.count())
