from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from python_web_final_project.accounts_app.models import CustomUserProxyCompany, CustomUserProxyApplicant
from python_web_final_project.applicants_app.models.main_models import ApplicantProfile, TechnicalSkill, OtherSkill, \
    EducationDetail, WorkExperienceDetail
from python_web_final_project.common_app.models import Job, JobApplication
from python_web_final_project.companies_app.models import CompanyProfile

UserModel = get_user_model()

admin.site.index_title = 'Job Market'
admin.site.site_title = 'Job Market'
admin.site.site_header = 'Job Market Admin'


class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile


class JobInline(admin.StackedInline):
    model = Job
    exclude = ('bookmarked_by',)


@admin.register(CustomUserProxyCompany)
class AdminCompanyUser(admin.ModelAdmin):
    list_display = ('name', 'email')
    fields = ('email',)

    inlines = (
        CompanyProfileInline,
        JobInline,
    )

    def get_queryset(self, request):
        return UserModel.objects.filter(is_company=True, is_superuser=False, is_staff=False)

    def name(self, obj):
        return obj.companyprofile.name

    name.admin_order_field = 'companyprofile'


class ApplicantProfileInline(admin.StackedInline):
    model = ApplicantProfile


class TechnicalSkillInline(admin.StackedInline):
    model = TechnicalSkill


class OtherSkillInline(admin.StackedInline):
    model = OtherSkill


class WorkExperienceInline(admin.StackedInline):
    model = WorkExperienceDetail


class EducationDetailInline(admin.StackedInline):
    model = EducationDetail


@admin.register(CustomUserProxyApplicant)
class ApplicantUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    fields = ('email',)

    inlines = (
        ApplicantProfileInline,
        WorkExperienceInline,
        EducationDetailInline,
        TechnicalSkillInline,
        OtherSkillInline,
    )

    def get_queryset(self, request):
        return UserModel.objects.filter(is_company=False, is_superuser=False, is_staff=False)

    def name(self, obj):
        return obj.applicantprofile.full_name

    name.admin_order_field = 'applicantprofile'

    def phone(self, obj):
        return obj.applicantprofile.phone


@admin.register(UserModel)
class AllUsersAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_superuser')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_superuser', 'is_staff', 'groups', 'is_company')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    search_fields = ['email']
    ordering = ['email']

