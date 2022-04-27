from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, CreateCompanyAndJobMixin


class TestBookmarkJobView(TestCase, CreateUserAndProfileMixin, CreateCompanyAndJobMixin):

    def setUp(self):
        self.user = self._create_user()
        self.profile = self._create_profile(self.user)
        self.company = self._create_company()
        self.job = self._create_job(self.company)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.response = self.client.post(reverse('bookmark', kwargs={'pk': self.job.pk}), {},
                                         HTTP_REFERER=reverse('index'))

    def test_user_bookmarks_job_on_index_page_expect_job_to_be_in_users_bookmarks_and_redirect_to_index(self):
        self.assertEqual(self.user, self.job.bookmarked_by.first())
        self.assertRedirects(self.response, reverse('index'))

    def test_user_removes_bookmark_on_index_expect_bookmark_to_be_removed_and_redirect_to_index(self):
        response = self.client.post(reverse('bookmark', kwargs={'pk': self.job.pk}), {}, HTTP_REFERER=reverse('index'))
        self.assertEqual(0, self.job.bookmarked_by.count())
        self.assertRedirects(response, reverse('index'))