from django.test import TestCase
from django.urls import reverse

from python_web_final_project.applicants_app.views.main_views import ApplicantBookmarkedJobsView
from python_web_final_project.common_app.models import Job
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, CreateCompanyAndJobMixin


class TestApplicantBookmarkedJobsView(TestCase, CreateUserAndProfileMixin, CreateCompanyAndJobMixin):

    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)
        self.company = self._create_company()
        self.job = self._create_job(self.company)

    def test_correct_title(self):
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('bookmarked jobs'))
        self.assertEqual('Job Market | My Bookmarks', response.context['title'])

    def test_user_has_no_bookmarks_expect_empty_queryset(self):
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('bookmarked jobs'))
        bookmarks = Job.objects.filter(bookmarked_by=self.user)
        self.assertQuerysetEqual(bookmarks, response.context_data['bookmarked_jobs'])

    def test_user_has_bookmarks_expect_correct_queryset(self):
        self.job.bookmarked_by.add(self.user)
        bookmarks = Job.objects.filter(bookmarked_by=self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('bookmarked jobs'))
        self.assertQuerysetEqual(bookmarks, response.context_data['bookmarked_jobs'])
