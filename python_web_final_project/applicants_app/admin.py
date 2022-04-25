from django.contrib import admin

# Register your models here.
from python_web_final_project.accounts_app.models import CustomUser
from python_web_final_project.applicants_app.models.main_models import EducationDetail, WorkExperienceDetail


class EducationDetailInline(admin.StackedInline):
    model = EducationDetail


class WorkExperienceDetailInline(admin.StackedInline):
    model = WorkExperienceDetail


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (
        WorkExperienceDetailInline,
        EducationDetailInline,
    )
