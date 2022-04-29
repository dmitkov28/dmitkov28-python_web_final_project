from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views

from python_web_final_project.applicants_app.forms import ApplicantEditProfileForm, ApplicantEditTechnicalSkillsFormset, \
    ApplicantEditOtherSkillsFormset, ApplicantSubmitJobApplicationForm, ApplicantEditEducationDetailFormset, \
    ApplicantEditWorkExperienceDetailFormset
from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.applicants_app.views.base_views import ApplicantAddEditSkillsBaseView, \
    ApplicantEditResumeBaseView
from python_web_final_project.common_app.models import Job, JobApplication
from python_web_final_project.helpers.mixins.custom_user_passes_test_mixins import UserIsApplicantTestMixin
from python_web_final_project.helpers.mixins.view_mixins import AddPageTitleMixin


class ApplicantEditProfileView(LoginRequiredMixin, UserIsApplicantTestMixin, AddPageTitleMixin, views.UpdateView):
    form_class = ApplicantEditProfileForm
    template_name = 'applicant_templates/edit-profile.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('applicant profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return ApplicantProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.add_page_title('Edit Applicant Profile')
        return context


class ApplicantEditTechnicalSkillsView(ApplicantAddEditSkillsBaseView):
    form_class = ApplicantEditTechnicalSkillsFormset
    h1 = 'Technical Skills'


class ApplicantEditOtherSkillsView(ApplicantAddEditSkillsBaseView):
    form_class = ApplicantEditOtherSkillsFormset
    h1 = 'Other Skills'


class ApplicantBookmarkedJobsView(LoginRequiredMixin, UserIsApplicantTestMixin, AddPageTitleMixin, views.ListView):
    template_name = 'applicant_templates/bookmarked-jobs.html'
    context_object_name = 'bookmarked_jobs'
    paginate_by = 5

    def get_queryset(self):
        bookmarked_jobs_by_user = Job.objects.filter(bookmarked_by=self.request.user).order_by('-date_added')
        return bookmarked_jobs_by_user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.add_page_title('My Bookmarks')
        return context


class ApplicantSubmitJobApplicationView(LoginRequiredMixin, UserIsApplicantTestMixin, AddPageTitleMixin,
                                        views.CreateView):
    model = JobApplication
    form_class = ApplicantSubmitJobApplicationForm
    template_name = 'applicant_templates/submit-job-application.html'
    success_url = reverse_lazy('job applications')

    def get_job(self):
        return get_object_or_404(Job, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['job'] = self.get_job()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.add_page_title(
            f'Apply for {self.get_job()} ({self.get_job().company.companyprofile.name}')
        context['job'] = self.get_job()
        return context


class ApplicantJobApplicationsView(LoginRequiredMixin, UserIsApplicantTestMixin, AddPageTitleMixin, views.ListView):
    template_name = 'applicant_templates/job-applications.html'
    context_object_name = 'job_applications'
    paginate_by = 5

    def get_queryset(self):
        user_job_applications = JobApplication.objects.filter(user=self.request.user).order_by('-date_added')
        return user_job_applications

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.add_page_title('My Job Applications')
        return context


class ApplicantEditEducationView(ApplicantEditResumeBaseView):
    template_name = 'applicant_templates/edit-education.html'
    form_class = ApplicantEditEducationDetailFormset


class ApplicantEditWorkExperienceView(ApplicantEditResumeBaseView):
    template_name = 'applicant_templates/edit-experience.html'
    form_class = ApplicantEditWorkExperienceDetailFormset


@login_required
def bookmark(request, pk):
    user = request.user
    job = Job.objects.get(pk=pk)
    if request.method == 'POST':
        if user not in job.bookmarked_by.all():
            job.bookmarked_by.add(user)
        else:
            job.bookmarked_by.remove(user)
        job.save()

    return redirect(request.META.get('HTTP_REFERER'))
