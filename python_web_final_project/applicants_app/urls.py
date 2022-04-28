from django.urls import path

import python_web_final_project.applicants_app.views.main_views

urlpatterns = (
    path('bookmarked-jobs', python_web_final_project.applicants_app.views.main_views.ApplicantBookmarkedJobsView.as_view(), name='bookmarked jobs'),
    path('job-applications', python_web_final_project.applicants_app.views.main_views.ApplicantJobApplicationsView.as_view(), name='job applications'),
    path('edit/profile', python_web_final_project.applicants_app.views.main_views.ApplicantEditProfileView.as_view(), name='edit applicant profile'),
    path('edit/education', python_web_final_project.applicants_app.views.main_views.ApplicantEditEducationView.as_view(), name='edit education'),
    path('edit/experience', python_web_final_project.applicants_app.views.main_views.ApplicantEditWorkExperienceView.as_view(), name='edit experience'),
    path('edit/technical-skills', python_web_final_project.applicants_app.views.main_views.ApplicantEditTechnicalSkillsView.as_view(), name='edit technical skills'),
    path('edit/other-skills', python_web_final_project.applicants_app.views.main_views.ApplicantEditOtherSkillsView.as_view(), name='edit other skills'),
    path('bookmark/<int:pk>', python_web_final_project.applicants_app.views.main_views.bookmark, name='bookmark'),
    path('application/job/<int:pk>', python_web_final_project.applicants_app.views.main_views.ApplicantSubmitJobApplicationView.as_view(), name='submit application'),
)
