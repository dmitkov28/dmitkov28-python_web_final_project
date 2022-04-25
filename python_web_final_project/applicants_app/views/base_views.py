from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic as views

from python_web_final_project.helpers.mixins.custom_user_passes_test_mixins import UserIsApplicantTestMixin


class ApplicantAddEditSkillsBaseView(LoginRequiredMixin, UserIsApplicantTestMixin, views.View):
    template_name = 'applicant_templates/edit-skills.html'
    h1 = None
    form_class = None

    def get(self, request):
        formset = self.form_class(instance=self.request.user)
        context = {
            'formset': formset,
            'h1': self.h1,
            'title': 'Job Market | Edit Skills',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        formset = self.form_class(request.POST, instance=self.request.user)
        if formset.is_valid():
            formset.save()
            return redirect('applicant profile', pk=self.request.user.pk)

        else:

            context = {
                'formset': formset,
                'h1': self.h1,
                'title': 'Job Market | Edit Skills'
            }

            return render(request, self.template_name, context)


class ApplicantEditResumeBaseView(LoginRequiredMixin, UserIsApplicantTestMixin, views.View):
    template_name = None
    form_class = None

    def get(self, request):
        formset = self.form_class(instance=self.request.user)
        context = {
            'formset': formset,
            'title': 'Job Market | Edit Resume'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        formset = self.form_class(request.POST, instance=self.request.user)
        if formset.is_valid():
            formset.save()
            return redirect('applicant profile', pk=self.request.user.pk)
        context = {
            'formset': formset,
            'title': 'Job Market | Edit Resume'
        }
        return render(request, self.template_name, context)