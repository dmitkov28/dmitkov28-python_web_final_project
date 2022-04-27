from django.test import TestCase
from django.urls import reverse

from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin


class TestLogoutView(TestCase, CreateUserAndProfileMixin):

    def test_logout_redirects_to_home(self):
        self._create_user()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(response.context['user'].is_authenticated)

