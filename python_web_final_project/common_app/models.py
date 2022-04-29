from cloudinary import models as cloudinary_models
from django.contrib.auth import get_user_model
from django.db import models

from python_web_final_project.companies_app.models import CompanyProfile

UserModel = get_user_model()


class Job(models.Model):
    ROLE_MAX_LENGTH = 120
    CATEGORY_MAX_LENGTH = 60
    LOCATION_MAX_LENGTH = 100

    EXPERIENCE_LEVELS = (
        'Entry',
        'Mid',
        'Intermediate',
        'Senior or Executive',
    )

    WORK_SCHEDULE = (
        'Part-Time',
        'Full-Time',
        'Flexible',
        'Shift Work',
    )

    class Meta:
        ordering = ['date_added']

    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
    )

    company = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    experience_level = models.CharField(
        choices=[(c, c) for c in EXPERIENCE_LEVELS],
        max_length=max([len(c) for c in EXPERIENCE_LEVELS]),
        null=True,
        blank=True,
    )

    description = models.TextField()

    responsibilities = models.TextField(
        null=True,
        blank=True,
    )

    work_schedule = models.CharField(
        choices=[(c, c) for c in WORK_SCHEDULE],
        max_length=max([len(c) for c in WORK_SCHEDULE]),
    )

    requirements = models.TextField(
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        null=True,
        blank=True,
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    bookmarked_by = models.ManyToManyField(
        to=UserModel,
        blank=True,
        related_name='bookmarked_by'
    )

    def __str__(self):
        return f'{self.role} ({self.date_added})'


class JobApplication(models.Model):
    message = models.TextField()

    cv = cloudinary_models.CloudinaryField(
        resource_type='',
        folder='application_documents',
        null=True,
        blank=True,
    )

    additional_documents = cloudinary_models.CloudinaryField(
        resource_type='',
        folder='application_documents',
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    job = models.ForeignKey(
        to=Job,
        on_delete=models.CASCADE,
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user} Application for {self.job}'

    class Meta:
        unique_together = ('user', 'job')
        verbose_name_plural = 'Job Applications'
