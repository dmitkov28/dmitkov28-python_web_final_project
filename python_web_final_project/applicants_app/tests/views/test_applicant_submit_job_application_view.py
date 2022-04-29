from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from python_web_final_project.applicants_app.forms import ApplicantSubmitJobApplicationForm
from python_web_final_project.applicants_app.views.main_views import ApplicantSubmitJobApplicationView
from python_web_final_project.common_app.models import JobApplication
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, CreateCompanyAndJobMixin


class TestApplicantSubmitJobApplicationView(TestCase, CreateUserAndProfileMixin, CreateCompanyAndJobMixin):
    INVALID_JOB_PK = 100

    def setUp(self):
        self.user = self._create_user()
        self.company = self._create_company()
        self.company_profile = self._create_company_profile(self.company)
        self.job = self._create_job(self.company)
        self.mock_file = SimpleUploadedFile(name='mock.pdf', content=b'')
        self.valid_form_data = {
            'message': 'message',
            'user': self.user,
            'job': self.job,
        }

        self.client.login(**self.VALID_USER_CREDENTIALS)

    def test_view_returns_correct_form(self):
        response = self.client.get(reverse('submit application', kwargs={'pk': self.job.pk}))
        form = response.context['form']
        expected_form_class = ApplicantSubmitJobApplicationForm
        self.assertIsInstance(form, expected_form_class)
        self.assertEqual(self.user, form.user)
        self.assertEqual(self.job, form.job)

    def test_get_with_non_existing_job_expect_404(self):
        response = self.client.get(reverse('submit application', kwargs={'pk': self.INVALID_JOB_PK}))
        self.assertEqual(404, response.status_code)

    def test_post_with_valid_data_expect_object_to_be_created_and_redirect_to_job_applications(self):
        response = self.client.post(reverse('submit application', kwargs={'pk': self.job.pk}), data=self.valid_form_data)
        job_application_obj = JobApplication.objects.first()
        self.assertEqual(job_application_obj.user, self.user)
        self.assertEqual(job_application_obj.job, self.job)
        self.assertEqual(job_application_obj.message, self.valid_form_data['message'])
        self.assertRedirects(response, reverse('job applications'))




