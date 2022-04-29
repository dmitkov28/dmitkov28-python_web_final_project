from django.urls import path

import python_web_final_project.common_app.views
from python_web_final_project.common_app import views
from python_web_final_project.applicants_app.views import main_views as applicant_views



urlpatterns = (
    path('', views.IndexView.as_view(), name='index'),
    path('company/<int:pk>', views.CompanyProfileView.as_view(), name='company profile'),
    path('company/<int:pk>/jobs', views.CompanyJobsView.as_view(), name='company jobs'),
    path('job/<int:pk>', views.JobDetailsView.as_view(), name='job details'),
    path('applicant/<int:pk>', python_web_final_project.common_app.views.ApplicantProfileView.as_view(), name='applicant profile'),
)