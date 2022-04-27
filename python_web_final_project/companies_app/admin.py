from django.contrib import admin

from python_web_final_project.common_app.models import Job
from python_web_final_project.companies_app.models import CompanyProfile


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'jobs_posted')

    def jobs_posted(self, obj):
        count = Job.objects.filter(company=obj.user).count()
        return count

    jobs_posted.short_description = 'Jobs'
