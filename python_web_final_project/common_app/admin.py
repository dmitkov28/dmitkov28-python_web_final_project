from django.contrib import admin

# Register your models here.
from python_web_final_project.common_app.models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(JobApplication)
class JobAdmin(admin.ModelAdmin):
    pass
