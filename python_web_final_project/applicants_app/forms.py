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
    USER_ALREADY_APPLIED_FOR_JOB_MESSAGE = 'User has already applied for this job.'

    class Meta:
        model = JobApplication
        exclude = ('job', 'user')

    def __init__(self, user, job, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.job = job

    def clean(self):
        if JobApplication.objects.filter(user=self.user, job=self.job).exists():
            raise ValidationError(self.USER_ALREADY_APPLIED_FOR_JOB_MESSAGE)

    def save(self, commit=True):
        application = super().save(commit=False)
        application.job = self.job
        application.user = self.user

        application.save()
        return application


ApplicantEditTechnicalSkillsFormset = inlineformset_factory(UserModel, TechnicalSkill, fields='__all__', extra=1)

ApplicantEditOtherSkillsFormset = inlineformset_factory(UserModel, OtherSkill, fields='__all__', extra=1)

ApplicantEditEducationDetailFormset = inlineformset_factory(UserModel, EducationDetail, fields='__all__', extra=1)

ApplicantEditWorkExperienceDetailFormset = inlineformset_factory(UserModel, WorkExperienceDetail, fields='__all__',
                                                                 extra=1)
