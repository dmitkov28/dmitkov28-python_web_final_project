from django.contrib import admin

from python_web_final_project.common_app.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_filter = ('role', 'company', 'date_added')
    list_display = ('role', 'company_name', 'date_added', 'job_applications')
    search_fields = ('role', 'company')
    exclude = ('bookmarked_by',)

    def company_name(self, obj):
        return obj.company.companyprofile.name
    company_name.admin_order_field = 'company'

    def job_applications(self, obj):
        return obj.jobapplication_set.count()
    job_applications.admin_order_field = 'jobapplication'






