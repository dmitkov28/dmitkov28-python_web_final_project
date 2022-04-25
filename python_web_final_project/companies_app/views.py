from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from python_web_final_project.accounts_app.views import UserRegisterView
from python_web_final_project.common_app.models import Job, JobApplication
from python_web_final_project.companies_app.forms import CompanyEditProfileForm, CompanyJobForm
from python_web_final_project.companies_app.models import CompanyProfile
from python_web_final_project.helpers.mixins.custom_user_passes_test_mixins import UserIsCompanyTestMixin, \
    user_is_company
from python_web_final_project.helpers.mixins.view_mixins import CompanyAddEditJobMixin


class CompanyRegisterView(UserRegisterView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_action'] = reverse_lazy('company register')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'is_company': True,
        }
        return kwargs


class CompanyEditProfileView(LoginRequiredMixin, UserIsCompanyTestMixin, views.UpdateView):
    form_class = CompanyEditProfileForm
    template_name = 'company_templates/edit-company-profile.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('company profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(CompanyProfile, pk=self.request.user.pk)


class CompanyAddJobView(LoginRequiredMixin, CompanyAddEditJobMixin, UserIsCompanyTestMixin, views.CreateView):

    def get_success_url(self):
        success_url = reverse_lazy('company jobs', kwargs={'pk': self.request.user.pk})
        return success_url


class CompanyEditJobView(LoginRequiredMixin, CompanyAddEditJobMixin, UserIsCompanyTestMixin, views.UpdateView):
    template_name = 'company_templates/add-job.html'
    form_class = CompanyJobForm

    def get_object(self, queryset=None):
        job = Job.objects.get(pk=self.kwargs['pk'])
        return job

    def get_success_url(self):
        return reverse_lazy('company jobs', kwargs={'pk': self.request.user.pk})


class CompanyJobApplicationsView(LoginRequiredMixin, UserIsCompanyTestMixin, views.ListView):
    template_name = 'company_templates/job-applications.html'
    context_object_name = 'job_applications'

    def get_queryset(self):
        job = self.kwargs['pk']
        return JobApplication.objects.filter(job=job).order_by('-date_added')


@login_required
@user_passes_test(user_is_company, login_url=reverse_lazy('index'))
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect(reverse_lazy('company jobs', kwargs={'pk': request.user.pk}))
    return redirect(reverse('job details', kwargs={'pk':job.pk}))
