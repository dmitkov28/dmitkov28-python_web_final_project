from python_web_final_project.companies_app.forms import CompanyJobForm


class DynamicPaginatorMixin:
    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        paginator = super().get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs)
        current_page = self.request.GET.get('page', 1)
        paginator.get_elided_page_range = paginator.get_elided_page_range(current_page)
        return paginator


class CompanyAddEditJobMixin:
    template_name = 'company_templates/add-job.html'
    form_class = CompanyJobForm

    def get_initial(self):
        initial = super().get_initial()
        initial['company'] = self.request.user.pk
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['submitter'] = self.request.user
        return kwargs