from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy
from django.views import generic as views

from python_web_final_project.accounts_app.forms import LoginForm, RegisterApplicantForm, RegisterCompanyForm
from python_web_final_project.helpers.mixins.custom_user_passes_test_mixins import UserIsAuthenticatedTestMixin


class UserLoginView(UserIsAuthenticatedTestMixin, auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


class UserRegisterBaseView(UserIsAuthenticatedTestMixin, views.CreateView):
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

class ApplicantRegisterView(UserRegisterBaseView):
    template_name = 'accounts/register.html'
    form_class = RegisterApplicantForm


class CompanyRegisterView(UserRegisterBaseView):
    template_name = 'accounts/register-company.html'
    form_class = RegisterCompanyForm



class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')
