from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin
from python_web_final_project.common_app.models import Job


class TestApplicantBookmarkedJobsView(CreateUserAndProfileMixin, TestCase):

    def setUp(self):
        self.user = self._create_user()

    def test_user_has_no_bookmarks_expect_empty_queryset(self):
        self._create_profile(self.user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('bookmarked jobs'))
        bookmarks = Job.objects.filter(bookmarked_by=self.user)
        self.assertQuerysetEqual(bookmarks, response.context_data['bookmarked_jobs'])

    def test_user_has_bookmarks_expect_correct_queryset(self):
        pass

