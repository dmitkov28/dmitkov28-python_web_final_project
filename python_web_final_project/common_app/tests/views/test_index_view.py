from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse

from python_web_final_project.common_app.models import Job
from python_web_final_project.common_app.views import IndexView
from python_web_final_project.helpers.mixins.test_mixins import CreateUserAndProfileMixin, CreateCompanyAndJobMixin
from python_web_final_project.helpers.mixins.view_mixins import DynamicPaginatorMixin


class TestIndexView(TestCase, CreateUserAndProfileMixin, CreateCompanyAndJobMixin):

    def test_correct_navbar_when_user_not_authenticated(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateNotUsed(response, 'partials/navbar/navbar_applicant.html')
        self.assertTemplateNotUsed(response, 'partials/navbar/navbar_company.html')

    def test_correct_navbar_when_user_is_applicant(self):
        self._create_user()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('index'))

        self.assertTemplateUsed(response, 'partials/navbar/navbar_applicant.html')
        self.assertTemplateNotUsed(response, 'partials/navbar/navbar_company.html')

    def test_correct_navbar_when_user_is_company(self):
        self._create_company()
        self.client.login(**self.VALID_COMPANY_CREDENTIALS)
        response = self.client.get(reverse('index'))

        self.assertTemplateNotUsed(response, 'partials/navbar/navbar_applicant.html')
        self.assertTemplateUsed(response, 'partials/navbar/navbar_company.html')

    def test_view_has_correct_pagination(self):
        response = self.client.get(reverse('index'))
        paginator = response.context_data['paginator']
        view = response.context_data['view']
        expected_items_per_page = IndexView.paginate_by
        self.assertIsInstance(paginator, Paginator)
        self.assertEqual(expected_items_per_page, paginator.per_page)
        self.assertTrue(issubclass(type(view), DynamicPaginatorMixin))


    def test_non_existing_paginator_page_expect_404(self):
        response = self.client.get(reverse('index') + '?page=100')
        self.assertEqual(404, response.status_code)

    def test_no_jobs_expect_empty_queryset(self):
        jobs = self.client.get(reverse('index')).context['jobs']
        self.assertEqual(0, len(jobs))

    def test_when_jobs_and_no_query_expect_correct_queryset(self):
        company = self._create_company()
        self._create_job(company)
        jobs = Job.objects.all()
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(jobs, response.context['jobs'])

    def test_when_jobs_and_no_query_expect_correct_h1(self):
        company = self._create_company()
        self._create_job(company)
        response = self.client.get(reverse('index'))
        expected_h1 = 'All Jobs (1)'
        self.assertEqual(expected_h1, response.context['h1'])

    def test_when_no_jobs_and_no_query_expect_correct_h1(self):
        response = self.client.get(reverse('index'))
        expected_h1 = 'All Jobs (0)'
        self.assertEqual(expected_h1, response.context['h1'])

    def test_when_jobs_and_query_expext_correct_queryset(self):
        company = self._create_company()
        self._create_job(company)
        job_2 = Job(
            role='Engineer',
            description='Engineering Job',
            company=company,
            work_schedule='Full-Time',
        )

        job_2.full_clean()
        job_2.save()
        expected_queryset = Job.objects.filter(role=job_2.role)

        response = self.client.get(reverse('index'), {'query': 'Engineer'})
        queryset = response.context['jobs']
        self.assertQuerysetEqual(expected_queryset, queryset)

    def test_when_jobs_and_query_expext_correct_h1(self):
        company = self._create_company()
        self._create_job(company)
        job_2 = Job(
            role='Engineer',
            description='Engineering Job',
            company=company,
            work_schedule='Full-Time',
        )

        job_2.full_clean()
        job_2.save()

        response = self.client.get(reverse('index'), {'query': 'Engineer'})
        expected_h1 = 'Results for \'Engineer\' (1)'
        self.assertEqual(expected_h1, response.context['h1'])














