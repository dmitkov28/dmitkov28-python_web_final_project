from django.urls import path

from python_web_final_project.companies_app import views

urlpatterns = (
    path('edit/profile', views.CompanyEditProfileView.as_view(), name='edit company profile'),
    path('add/job', views.CompanyAddJobView.as_view(), name='add job'),
    path('job/<int:pk>/edit', views.CompanyEditJobView.as_view(), name='edit job'),
    path('job/<int:pk>/delete', views.delete_job, name='delete job'),
    path('job/<int:pk>/applications', views.CompanyJobApplicationsView.as_view(), name='applications for job'),
)
