from django.test import TestCase
from django.urls import reverse

from python_web_final_project.applicants_app.models.main_models import EducationDetail, WorkExperienceDetail
from python_web_final_project.applicants_app.views.main_views import ApplicantProfileView
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, CreateCompanyAndJobMixin


class TestApplicantProfileView(TestCase, CreateUserAndProfileMixin, CreateCompanyAndJobMixin):
    INVALID_USER_PK = 1000

    def _create_education_detail(self, user):
        education_detail = EducationDetail(
            institution='School',
            program='Program',
            degree='PhD',
            grade='5',
            location='Sofia',
            start_date='2020-01-01',
            user=user,
        )

        education_detail.full_clean()
        education_detail.save()
        return education_detail

    def _create_experience_detail(self, user):
        experience_detail = WorkExperienceDetail(
            role='Role',
            company='Company',
            description='Description',
            location='Sofia',
            start_date='2020-01-01',
            user=user,
        )

        experience_detail.full_clean()
        experience_detail.save()

        return experience_detail

    def setUp(self):
        self.user = self._create_user()

    def test_get_user_not_logged_in_expect_redirect_to_login(self):
        self._create_profile(self.user)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.user.pk}))
        self.assertRedirects(response, reverse('login') + f'?next=%2Fapplicant%2F{self.user.pk}')

    def test_get_super_user_expect_redirect_to_home(self):
        superuser = self._create_superuser()
        self.client.login(**self.VALID_SUPERUSER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': superuser.pk}))
        self.assertRedirects(response, reverse('index'))

    def test_get_super_user_expect_message_to_create_profile_manually_is_shown(self):
        superuser = self._create_superuser()
        self.client.login(**self.VALID_SUPERUSER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': superuser.pk}), follow=True)
        expected_message = ApplicantProfileView.SUPERUSER_MESSAGE
        self.assertContains(response, expected_message)

    def test_get_user_authenticated_correct_profile_expect_200(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(200, response.status_code)


    def test_get_user_authenticated_and_existing_profile_expect_can_edit_to_be_true(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.user.pk}))
        can_edit = response.context['can_edit']
        self.assertTrue(can_edit)


    def test_correct_template_is_shown(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(response, 'applicant_templates/profile.html')
        self.assertTemplateUsed(response, 'partials/navbar/navbar_applicant.html')
        self.assertTemplateNotUsed(response, 'partials/navbar/navbar_company.html')

    def test_correct_title_is_shown(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.user.pk}))
        expected_title = 'Job Market | Profile'
        title = response.context['title']
        self.assertEqual(expected_title, title)

    def test_user_authenticated_get_non_existing_profile_expect_redirect_to_own_profile(self):
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.INVALID_USER_PK}))
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, reverse('applicant profile', kwargs={'pk': self.user.pk}))

    def test_get_user_is_company_and_profile_does_not_exist_expect_404(self):
        self._create_company()
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.INVALID_USER_PK}))
        self.assertEqual(404, response.status_code)

    def test_get_profile_with_no_education_and_no_work_experience_expect_empty_querysets(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(0, len(response.context['education']))
        self.assertEqual(0, len(response.context['experience']))

    def test_get_profile_with_education_and_work_experience_expect_correct_context(self):
        self._create_profile(self.user)
        self._create_education_detail(self.user)
        self._create_experience_detail(self.user)
        education = EducationDetail.objects.filter(user=self.user).order_by('-start_date')
        experience = WorkExperienceDetail.objects.filter(user=self.user).order_by('-start_date')
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('applicant profile', kwargs={'pk': self.user.pk}))
        self.assertQuerysetEqual(education, response.context['education'])
        self.assertQuerysetEqual(experience, response.context['experience'])
