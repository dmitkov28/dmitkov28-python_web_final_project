from django import forms
from django.core.exceptions import ValidationError

from python_web_final_project.common_app.models import Job
from python_web_final_project.companies_app.models import CompanyProfile


class CompanyEditProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ('user',)


class CompanyJobForm(forms.ModelForm):
    INVALID_USER_MESSAGE = 'Invalid user.'

    class Meta:
        model = Job
        exclude = ('bookmarked_by',)

    def __init__(self, submitter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitter = submitter
        self.fields['company'].widget = forms.HiddenInput()

    def clean(self):
        company = self.cleaned_data.get('company', None)
        if company:
            if company.pk != self.submitter.companyprofile.pk:
                raise ValidationError(self.INVALID_USER_MESSAGE)
