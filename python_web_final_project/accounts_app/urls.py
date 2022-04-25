from django.urls import path
from python_web_final_project.accounts_app import views
from python_web_final_project.accounts_app import views

urlpatterns = (
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register/applicant', views.ApplicantRegisterView.as_view(), name='register applicant'),
    path('register/company', views.CompanyRegisterView.as_view(), name='register company'),

    path('logout', views.UserLogoutView.as_view(), name='logout'),
)