from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.companies_app.models import CompanyProfile

UserModel = get_user_model()


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class RegisterForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2', 'is_company')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_company'].widget = forms.HiddenInput()

    def save(self, commit=True):
        user = super().save(commit=True)
        if not user.is_company:
            profile = ApplicantProfile(user=user)

        else:
            profile = CompanyProfile(user=user)

        if commit:
            profile.save()
        return user
