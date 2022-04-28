from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.shortcuts import get_object_or_404
from django.views import generic as views

from python_web_final_project.common_app.models import Job
from python_web_final_project.companies_app.models import CompanyProfile
from python_web_final_project.helpers.mixins.view_mixins import DynamicPaginatorMixin


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


class CompanyProfileView(views.DetailView):
    template_name = 'company_templates/company-profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile_pk = self.kwargs['pk']
        return get_object_or_404(CompanyProfile, pk=profile_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = True if self.get_object().user == self.request.user else False
        return context


class CompanyJobsView(views.ListView):
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
        return context


class JobDetailsView(views.DetailView):
    template_name = 'common_templates/job-details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Job, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_apply'] = True if (
                    self.request.user.is_authenticated and not self.request.user.is_company) else False
        context['can_edit'] = True if self.request.user == self.get_object().company else False
        return context
