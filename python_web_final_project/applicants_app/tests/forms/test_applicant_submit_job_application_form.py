from django.test import TestCase

from python_web_final_project.applicants_app.forms import ApplicantSubmitJobApplicationForm
from python_web_final_project.common_app.models import JobApplication
from python_web_final_project.helpers.mixins import test_mixins


class TestApplicantSubmitJobApplicationForm(TestCase, test_mixins.CreateCompanyAndJobMixin,
                                            test_mixins.CreateUserAndProfileMixin):

    def setUp(self):
        self.user = self._create_user()
        self.company = self._create_company()
        self.job = self._create_job(self.company)
        self.valid_form_data = {
            'message': 'message',
            'user': self.user,
            'job': self.job,
        }

    def test_valid_data_expect_form_valid(self):
        form = ApplicantSubmitJobApplicationForm(
            submitter=self.user,
            job=self.job,
            data=self.valid_form_data,
        )

        self.assertTrue(form.is_valid())

    def test_valid_data_expect_object_saved(self):
        form = ApplicantSubmitJobApplicationForm(
            submitter=self.user,
            job=self.job,
            data=self.valid_form_data,
        )
        form.save()
        job_application = JobApplication.objects.first()

        self.assertEqual(job_application.job, self.job)
        self.assertEqual(job_application.user, self.user)
        self.assertEqual(job_application.message, 'message')

    def test_invalid_user_expect_form_invalid(self):
        pass
