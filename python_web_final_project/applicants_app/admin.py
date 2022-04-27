from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from python_web_final_project.accounts_app.models import CustomUser
from python_web_final_project.applicants_app.models.main_models import EducationDetail, WorkExperienceDetail, \
    ApplicantProfile, TechnicalSkill, OtherSkill

UserModel = get_user_model()

class ApplicantProfileInline(admin.StackedInline):
    model = ApplicantProfile

class TechnicalSkillInline(admin.StackedInline):
    model = TechnicalSkill

class OtherSkillInline(admin.StackedInline):
    model = OtherSkill

class EducationDetailInline(admin.StackedInline):
    model = EducationDetail


class WorkExperienceDetailInline(admin.StackedInline):
    model = WorkExperienceDetail


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (
        ApplicantProfileInline,
        WorkExperienceDetailInline,
        EducationDetailInline,
        TechnicalSkillInline,
        OtherSkillInline,
    )

    def get_queryset(self, request):
        return UserModel.objects.filter(is_company=False)
