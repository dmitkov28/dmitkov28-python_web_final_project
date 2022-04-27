from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from python_web_final_project.applicants_app.forms import ApplicantSubmitJobApplicationForm
from python_web_final_project.common_app.models import JobApplication
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, CreateCompanyAndJobMixin


class TestApplicantSubmitJobApplicationForm(TestCase, CreateCompanyAndJobMixin,
                                            CreateUserAndProfileMixin):

    def setUp(self):
        self.user = self._create_user()
        self.company = self._create_company()
        self.job = self._create_job(self.company)
        self.mock_file = SimpleUploadedFile(name='mock.pdf', content=b'')
        self.valid_job_application_form_data = {
            'message': 'message',
            'user': self.user,
            'job': self.job,
            'cv': self.mock_file,
        }

    def test_form_with_valid_data_expect_form_to_be_valid(self):
        form = ApplicantSubmitJobApplicationForm(
            user=self.user,
            job=self.job,
            data=self.valid_job_application_form_data,
        )

        self.assertTrue(form.is_valid())

    def test_valid_data_expect_job_application_object_to_be_saved(self):
        form = ApplicantSubmitJobApplicationForm(
            user=self.user,
            job=self.job,
            data=self.valid_job_application_form_data,
        )
        form.save()
        job_application = JobApplication.objects.first()

        self.assertEqual(job_application.job, self.job)
        self.assertEqual(job_application.user, self.user)
        self.assertEqual(job_application.message, 'message')

    def test_user_already_applied_expect_form_to_be_invalid(self):
        form = ApplicantSubmitJobApplicationForm(
            user=self.user,
            job=self.job,
            data=self.valid_job_application_form_data,
        )
        form.save()

        form = ApplicantSubmitJobApplicationForm(
            user=self.user,
            job=self.job,
            data=self.valid_job_application_form_data,
        )

        expected_error_message = ApplicantSubmitJobApplicationForm.USER_ALREADY_APPLIED_FOR_JOB_MESSAGE

        self.assertFalse(form.is_valid())
        self.assertEqual(expected_error_message, form.non_field_errors()[0])
