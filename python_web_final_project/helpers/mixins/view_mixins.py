from python_web_final_project.companies_app.forms import CompanyAddEditJobForm


class DynamicPaginatorMixin:
    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        paginator = super().get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs)
        current_page = self.request.GET.get('page', 1)
        paginator.get_elided_page_range = paginator.get_elided_page_range(current_page)
        return paginator


class CompanyAddEditJobViewMixin:
    template_name = 'company_templates/add-edit-job.html'
    form_class = CompanyAddEditJobForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user
        return kwargs
