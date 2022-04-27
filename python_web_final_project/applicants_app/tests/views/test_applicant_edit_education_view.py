from django.test import TestCase
from django.urls import reverse

from python_web_final_project.applicants_app.models.main_models import EducationDetail
from python_web_final_project.applicants_app.views.main_views import ApplicantEditEducationView
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, FormsetTestDataMixin


class TestApplicantEditEducationView(TestCase, CreateUserAndProfileMixin, FormsetTestDataMixin):
    VALID_FORMSET_DATA = {
        'educationdetail_set-TOTAL_FORMS': '1',
        'educationdetail_set-INITIAL_FORMS': '0',
        'educationdetail_set-MIN_NUM_FORMS': '0',
        'educationdetail_set-MAX_NUM_FORMS': '1000',
        'educationdetail_set-0-id': '',
        'educationdetail_set-0-institution': 'Some University',
        'educationdetail_set-0-degree': 'PhD',
        'educationdetail_set-0-program': 'Program',
        'educationdetail_set-0-grade': '6',
        'educationdetail_set-0-start_date': '2020-01-01',
        'educationdetail_set-0-end_date': '2022-01-01',
        'educationdetail_set-0-location': 'Sofia',
    }

    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)

    def test_correct_title(self):
        response = self.client.get(reverse('edit education'))
        expected_title = 'Job Market | Edit Resume'
        self.assertEqual(expected_title, response.context['title'])

    def test_post_valid_data_expect_data_to_be_created_and_redirect_to_profile(self):
        response = self.client.post(reverse('edit education'), data=self.VALID_EDUCATION_FORMSET_DATA)
        education_detail_qs = EducationDetail.objects.filter(user=self.user)
        education_detail_obj = education_detail_qs.first()
        self.assertTrue(education_detail_qs.exists())
        self.assertEqual(education_detail_obj.institution, self.VALID_FORMSET_DATA['educationdetail_set-0-institution'])
        self.assertEqual(education_detail_obj.degree, self.VALID_FORMSET_DATA['educationdetail_set-0-degree'])
        self.assertEqual(education_detail_obj.program, self.VALID_FORMSET_DATA['educationdetail_set-0-program'])
        self.assertRedirects(response, reverse('applicant profile', kwargs={'pk': self.user.pk}))

    def test_post_invalid_data_expect_object_not_to_be_created(self):
        self.client.post(reverse('edit education'), data=self.INVALID_EDUCATION_FORMSET_DATA)
        self.assertEqual(0, EducationDetail.objects.count())
