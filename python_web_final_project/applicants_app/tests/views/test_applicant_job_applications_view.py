from django.test import TestCase
from django.urls import reverse

from python_web_final_project.common_app.models import JobApplication
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, CreateCompanyAndJobMixin


class TestApplicantJobApplicationsView(TestCase, CreateUserAndProfileMixin, CreateCompanyAndJobMixin):

    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)

    def test_correct_title_is_shown(self):
        response = self.client.get(reverse('job applications'))
        expected_title = 'Job Market | My Job Applications'
        self.assertEqual(expected_title, response.context['title'])

    def test_no_job_applications_expect_empty_queryset(self):
        response = self.client.get(reverse('job applications'))
        job_applications = response.context['job_applications']
        self.assertEqual(0, len(job_applications))

    def test_profile_with_job_applications_expect_correct_queryset(self):
        company = self._create_company()
        job = self._create_job(company)
        job_application = JobApplication(
            user=self.user,
            job=job,
            message='Message',
        )

        job_application.full_clean()
        job_application.save()

        user_job_applications_queryset = JobApplication.objects.filter(user=self.user)

        response = self.client.get(reverse('job applications'))
        self.assertQuerysetEqual(user_job_applications_queryset, response.context['job_applications'])
