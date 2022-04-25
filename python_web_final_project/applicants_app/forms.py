import cloudinary.uploader
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from python_web_final_project.applicants_app.models.main_models import ApplicantProfile, TechnicalSkill, OtherSkill, \
    EducationDetail, WorkExperienceDetail
from python_web_final_project.common_app.models import JobApplication

UserModel = get_user_model()


class ApplicantEditProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        exclude = ('user',)


class ApplicantSubmitJobApplicationForm(forms.ModelForm):
    INVALID_USER_MESSAGE = 'Invalid user.'
    INVALID_JOB_MESSAGE = 'Invalid job.'

    class Meta:
        model = JobApplication
        fields = '__all__'

    def __init__(self, submitter, job, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitter = submitter
        self.job = job
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['job'].widget = forms.HiddenInput()

    def clean(self):
        if self.cleaned_data.get('user', None) != self.submitter:
            raise ValidationError(self.INVALID_USER_MESSAGE)

        if self.cleaned_data.get('job', None) != self.job:
            raise ValidationError(self.INVALID_JOB_MESSAGE)

        return super().clean()


ApplicantEditTechnicalSkillsFormset = inlineformset_factory(UserModel, TechnicalSkill, fields='__all__', extra=1)

ApplicantEditOtherSkillsFormset = inlineformset_factory(UserModel, OtherSkill, fields='__all__', extra=1)

ApplicantEditEducationDetailFormset = inlineformset_factory(UserModel, EducationDetail, fields='__all__', extra=1)

ApplicantEditWorkExperienceDetailFormset = inlineformset_factory(UserModel, WorkExperienceDetail, fields='__all__',
                                                                 extra=1)
