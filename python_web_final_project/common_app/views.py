from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.shortcuts import get_object_or_404, redirect
from django.views import generic as views

from python_web_final_project.applicants_app.models.main_models import ApplicantProfile, EducationDetail, \
    WorkExperienceDetail
from python_web_final_project.common_app.models import Job
from python_web_final_project.companies_app.models import CompanyProfile
from python_web_final_project.helpers.mixins.view_mixins import DynamicPaginatorMixin, AddPageTitleMixin


class IndexView(DynamicPaginatorMixin, views.ListView):
    template_name = 'common_templates/index.html'
    model = Job
    context_object_name = 'jobs'
    paginate_by = 5

    def get_search_query(self):
        return self.request.GET.get('query')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.get_search_query():
            context['h1'] = f'All Jobs ({self.get_queryset().count()})'
        else:
            context['h1'] = f'Results for \'{self.get_search_query()}\' ({self.get_queryset().count()})'

        return context

    def get_queryset(self):
        q = self.get_search_query()
        vector = SearchVector('role', 'description')
        query = SearchQuery(q)
        if q:
            queryset = super().get_queryset().annotate(search=vector).filter(search=query).order_by('-date_added')
        else:
            queryset = super().get_queryset().filter().order_by('-date_added')
        return queryset


class ApplicantProfileView(LoginRequiredMixin, AddPageTitleMixin, views.DetailView):
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
        context['title'] = self.add_page_title(self.get_object().full_name)
        return context


class CompanyProfileView(views.DetailView, AddPageTitleMixin):
    template_name = 'company_templates/company-profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile_pk = self.kwargs['pk']
        return get_object_or_404(CompanyProfile, pk=profile_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = True if self.get_object().user == self.request.user else False
        context['title'] = self.add_page_title(self.get_object().name)
        return context


class CompanyJobsView(views.ListView, AddPageTitleMixin):
    template_name = 'common_templates/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5

    def get_profile(self):
        profile = get_object_or_404(CompanyProfile, pk=self.kwargs['pk'])
        return profile

    def get_queryset(self):
        queryset = Job.objects.filter(company=self.get_profile().user).order_by('-date_added')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        context['can_edit'] = self.get_profile().user == self.request.user
        context['title'] = self.add_page_title(f'Jobs by {self.get_profile().name}')
        return context


class JobDetailsView(views.DetailView, AddPageTitleMixin):
    template_name = 'common_templates/job-details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Job, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_apply'] = True if (
                self.request.user.is_authenticated and not self.request.user.is_company) else False
        context['can_edit'] = True if self.request.user == self.get_object().company else False
        context['title'] = self.add_page_title(
            f'{self.get_object().role} ({self.get_object().company.companyprofile.name})')
        return context
