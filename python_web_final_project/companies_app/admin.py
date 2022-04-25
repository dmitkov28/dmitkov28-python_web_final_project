from django.contrib import admin

# Register your models here.
from python_web_final_project.companies_app.models import CompanyProfile


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    pass

