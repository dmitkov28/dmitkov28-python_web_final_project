from django.test import TestCase
from django.urls import reverse

from python_web_final_project.applicants_app.models.main_models import TechnicalSkill
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, FormsetTestDataMixin



class TestEditTechnicalSkillsView(TestCase, CreateUserAndProfileMixin):
    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)
        self.VALID_TECHNICAL_SKILL_FORMSET_DATA = {
            'technicalskill_set-0-name': 'Django',
            'technicalskill_set-0-level': 60,
            'technicalskill_set-TOTAL_FORMS': '1',
            'technicalskill_set-INITIAL_FORMS': '0',
            'technicalskill_set-MIN_NUM_FORMS': '0',
            'technicalskill_set-MAX_NUM_FORMS': '1000',
        }

    def test_post_valid_data_expect_object_to_be_created_and_redirect_to_profile(self):
        data = self.VALID_TECHNICAL_SKILL_FORMSET_DATA
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('edit technical skills'), data=data)
        skill_obj = TechnicalSkill.objects.first()
        self.assertRedirects(response, reverse('applicant profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(skill_obj.name, self.VALID_TECHNICAL_SKILL_FORMSET_DATA['technicalskill_set-0-name'])
        self.assertEqual(skill_obj.level, self.VALID_TECHNICAL_SKILL_FORMSET_DATA['technicalskill_set-0-level'])
        self.assertEqual(skill_obj.user, self.user)


    def test_post_invalid_data_expect_object_not_to_be_created(self):
        data = self.VALID_TECHNICAL_SKILL_FORMSET_DATA
        data['technicalskill_set-0-level'] = 700
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.post(reverse('edit technical skills'), data=data, follow=True)
        self.assertEqual(0, TechnicalSkill.objects.count())

