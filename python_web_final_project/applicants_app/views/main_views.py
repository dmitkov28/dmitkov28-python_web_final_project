from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views

from python_web_final_project.applicants_app.forms import ApplicantEditProfileForm, ApplicantEditTechnicalSkillsFormset, \
    ApplicantEditOtherSkillsFormset, ApplicantSubmitJobApplicationForm, ApplicantEditEducationDetailFormset, \
    ApplicantEditWorkExperienceDetailFormset
from python_web_final_project.applicants_app.models.main_models import ApplicantProfile, EducationDetail, \
    WorkExperienceDetail
from python_web_final_project.applicants_app.views.base_views import ApplicantAddEditSkillsBaseView, \
    ApplicantEditResumeBaseView
from python_web_final_project.common_app.models import Job, JobApplication
from python_web_final_project.helpers.mixins.custom_user_passes_test_mixins import UserIsApplicantTestMixin


class ApplicantProfileView(LoginRequiredMixin, views.DetailView):
    model = ApplicantProfile
    template_name = 'applicant_templates/profile.html'
    context_object_name = 'profile'
    SUPERUSER_MESSAGE = 'Superusers must create their profiles manually in the admin section.'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            try:
                ApplicantProfile.objects.get(pk=self.request.user.pk)
            except ApplicantProfile.DoesNotExist:
                messages.warning(request, self.SUPERUSER_MESSAGE)
                return redirect('index')

            return super().dispatch(request, *args, **kwargs)

        if self.request.user.is_authenticated and not self.request.user.is_company and self.request.user.pk != \
                self.kwargs['pk']:
            return redirect('applicant profile', pk=self.request.user.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        profile = get_object_or_404(ApplicantProfile, pk=pk)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        education = EducationDetail.objects.filter(user=self.request.user).order_by('-start_date')
        experience = WorkExperienceDetail.objects.filter(user=self.request.user).order_by('-start_date')
        context['can_edit'] = self.request.user == self.get_object().user
        context['education'] = education
        context['experience'] = experience
        context['title'] = 'Job Market | Profile'
        return context


class ApplicantEditProfileView(LoginRequiredMixin, UserIsApplicantTestMixin, views.UpdateView):
    form_class = ApplicantEditProfileForm
    template_name = 'applicant_templates/edit-profile.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('applicant profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return ApplicantProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Job Market | Edit Profile'
        return context


class ApplicantEditTechnicalSkillsView(ApplicantAddEditSkillsBaseView):
    form_class = ApplicantEditTechnicalSkillsFormset
    h1 = 'Technical Skills'


class ApplicantEditOtherSkillsView(ApplicantAddEditSkillsBaseView):
    form_class = ApplicantEditOtherSkillsFormset
    h1 = 'Other Skills'


class ApplicantBookmarkedJobsView(LoginRequiredMixin, UserIsApplicantTestMixin, views.ListView):
    template_name = 'applicant_templates/bookmarked-jobs.html'
    context_object_name = 'bookmarked_jobs'
    paginate_by = 5

    def get_queryset(self):
        bookmarked_jobs_by_user = Job.objects.filter(bookmarked_by=self.request.user)
        return bookmarked_jobs_by_user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Job Market | My Bookmarks'
        return context


class ApplicantSubmitJobApplicationView(LoginRequiredMixin, UserIsApplicantTestMixin, views.CreateView):
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
        context['title'] = 'Job Market | Apply for Job'
        context['job'] = self.get_job()
        return context


class ApplicantJobApplications(LoginRequiredMixin, UserIsApplicantTestMixin, views.ListView):
    template_name = 'applicant_templates/job-applications.html'
    context_object_name = 'job_applications'
    paginate_by = 5

    def get_queryset(self):
        user_job_applications = JobApplication.objects.filter(user=self.request.user).order_by('-date_added')
        return user_job_applications

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Job Market | My Applications'
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
    if user not in job.bookmarked_by.all():
        job.bookmarked_by.add(user)
    else:
        job.bookmarked_by.remove(user)
    job.save()

    return redirect(request.META.get('HTTP_REFERER'))
