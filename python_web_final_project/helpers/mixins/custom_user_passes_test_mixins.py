from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserIsAuthenticatedTestMixin(UserPassesTestMixin):

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')


class UserIsCompanyTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_company

    def handle_no_permission(self):
        return redirect('index')


class UserIsApplicantTestMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_company

    def handle_no_permission(self):
        return redirect('index')


def user_is_company(user):
    return user.is_company


def user_is_applicant(user):
    return not user.is_company
