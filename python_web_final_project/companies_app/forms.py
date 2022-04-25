from django import forms

from python_web_final_project.common_app.models import Job
from python_web_final_project.companies_app.models import CompanyProfile


class CompanyEditProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ('user',)


class CompanyAddEditForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('company', 'bookmarked_by',)

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company = company

    def save(self, commit=True):
        job = super().save(commit=False)

        job.company = self.company
        job.save()

        return job
