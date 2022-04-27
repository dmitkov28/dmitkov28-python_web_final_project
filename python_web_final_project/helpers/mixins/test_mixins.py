import datetime

from django.contrib.auth import get_user_model

from python_web_final_project.applicants_app.models.main_models import ApplicantProfile
from python_web_final_project.common_app.models import Job
from python_web_final_project.companies_app.models import CompanyProfile

UserModel = get_user_model()




class CreateUserAndProfileMixin:
    VALID_REGISTER_DATA = {
        'email': 'user@mail.com',
        'password1': '_qWe!@&#l>10pr_',
        'password2': '_qWe!@&#l>10pr_',
    }

    INVALID_REGISTER_DATA = {
        'email': 'user',
        'password1': '_qWe!@&#l>pr_',
        'password2': '_qWe!@&#l>10pr_',
    }

    VALID_COMPANY_REGISTER_DATA = {
        'email': 'company@mail.com',
        'password1': '_qWe!@&#l>10pr_',
        'password2': '_qWe!@&#l>10pr_',
        'company_name': 'Company'
    }

    INVALID_COMPANY_REGISTER_DATA = {
        'email': 'company',
        'password1': '_qWe@&#l>10pr_',
        'password2': '_qWe!@&#l0pr_',
        'company_name': 'Company'
    }

    VALID_USER_CREDENTIALS = {
        'email': 'testuser@mail.com',
        'password': '123456qwe',
    }

    VALID_COMPANY_CREDENTIALS = {
        'email': 'company@mail.com',
        'password': '123456qwe',
    }

    VALID_SUPERUSER_CREDENTIALS = {
        'email': 'superuser@mail.com',
        'password': '123456qwe',
    }

    def _create_user(self):
        return UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

    def _create_superuser(self):
        return UserModel.objects.create_superuser(**self.VALID_SUPERUSER_CREDENTIALS)

    def _create_profile(self, user):
        profile = ApplicantProfile(
            user=user,
        )
        profile.full_clean()
        profile.save()
        return profile


class CreateCompanyAndJobMixin:
    VALID_COMPANY_CREDENTIALS = {
        'email': 'company@mail.com',
        'password': '123456qwe',
    }

    def _create_company(self, **credentials):
        company = UserModel.objects.create_user(**self.VALID_COMPANY_CREDENTIALS if not credentials else credentials)
        company.is_company = True
        company.full_clean()
        company.save()
        return company

    def _create_company_profile(self, company):
        profile = CompanyProfile(user=company)
        profile.full_clean()
        profile.save()
        return profile

    def _create_job(self, company):
        job = Job(
            role='Job Role',
            description='Job Description',
            experience_level='Entry',
            responsibilities='Job Responsibilities',
            work_schedule='Full-Time',
            requirements='Job Requirements',
            location='Job Location',
            date_added=datetime.datetime.now(),
            company=company,
        )

        job.full_clean()
        job.save()

        return job


class FormsetTestDataMixin:
    VALID_TECHNICAL_SKILL_FORMSET_DATA = {
        'technicalskill_set-0-name': 'Django',
        'technicalskill_set-0-level': 60,
        'technicalskill_set-TOTAL_FORMS': '1',
        'technicalskill_set-INITIAL_FORMS': '0',
        'technicalskill_set-MIN_NUM_FORMS': '0',
        'technicalskill_set-MAX_NUM_FORMS': '1000',
    }

    INVALID_TECHNICAL_SKILL_FORMSET_DATA = {
        'technicalskill_set-0-name': 'Django',
        'technicalskill_set-0-level': 600,
        'technicalskill_set-TOTAL_FORMS': '1',
        'technicalskill_set-INITIAL_FORMS': '0',
        'technicalskill_set-MIN_NUM_FORMS': '0',
        'technicalskill_set-MAX_NUM_FORMS': '1000',
    }

    VALID_EDUCATION_FORMSET_DATA = {
        'educationdetail_set-TOTAL_FORMS': '1',
        'educationdetail_set-INITIAL_FORMS': '0',
        'educationdetail_set-MIN_NUM_FORMS': '0',
        'educationdetail_set-MAX_NUM_FORMS': '1000',
        'educationdetail_set-0-id': '',
        'educationdetail_set-0-institution': 'Some University',
        'educationdetail_set-0-degree': 'PhD',
        'educationdetail_set-0-program': 'Program',
        'educationdetail_set-0-grade': '6',
        'educationdetail_set-0-start_date': '2020-01-01',
        'educationdetail_set-0-end_date': '2022-01-01',
        'educationdetail_set-0-location': 'Sofia',
    }

    INVALID_EDUCATION_FORMSET_DATA = {
        'educationdetail_set-TOTAL_FORMS': '1',
        'educationdetail_set-INITIAL_FORMS': '0',
        'educationdetail_set-MIN_NUM_FORMS': '0',
        'educationdetail_set-MAX_NUM_FORMS': '1000',
        'educationdetail_set-0-id': '',
        'educationdetail_set-0-institution': 'Some University',
        'educationdetail_set-0-degree': 'PhD',
        'educationdetail_set-0-program': 'Program',
        'educationdetail_set-0-grade': '6',
        'educationdetail_set-0-start_date': '',
        'educationdetail_set-0-end_date': '2022-01-01',
        'educationdetail_set-0-location': 'Sofia',
    }
