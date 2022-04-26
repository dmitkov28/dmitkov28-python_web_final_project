from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError

from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.companies_app.models import CompanyProfile

UserModel = get_user_model()


class LoginForm(auth_forms.AuthenticationForm):
    pass


class RegisterBaseForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')


class RegisterApplicantForm(RegisterBaseForm):

    def save(self, commit=True):
        user = super().save(commit=True)
        profile = ApplicantProfile(user=user)
        profile.save()
        return user


class RegisterCompanyForm(RegisterBaseForm):
    COMPANY_EXISTS_MESSAGE = 'A company with this name already exists.'

    company_name = forms.CharField(
        max_length=CompanyProfile.COMPANY_NAME_MAX_LENGTH,
    )

    def clean(self):
        if CompanyProfile.objects.filter(name=self.cleaned_data['company_name']).exists():
            raise ValidationError(self.COMPANY_EXISTS_MESSAGE)

        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        user.save()

        profile = CompanyProfile(
            name=self.cleaned_data['company_name'],
            user=user,
        )

        profile.save()
        return user
