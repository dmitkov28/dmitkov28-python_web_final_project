from cloudinary import models as cloudinary_models
from django.contrib.auth import get_user_model
from django.db import models

from python_web_final_project.applicants_app.models.base_models import SkillsBaseModel

UserModel = get_user_model()


class ApplicantProfile(models.Model):
    FIRST_NAME_MAX_LENGTH = 35
    LAST_NAME_MAX_LENGTH = 35
    CURRENT_OCCUPATION_MAX_LENGTH = 65
    ADDRESS_MAX_LENGTH = 255
    PHONE_MAX_LENGTH = 13

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        null=True,
        blank=True,
    )

    current_occupation = models.CharField(
        max_length=CURRENT_OCCUPATION_MAX_LENGTH,
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        null=True,
        blank=True,
    )

    linkedin_profile = models.URLField(
        blank=True,
        null=True,
    )

    personal_website = models.URLField(
        blank=True,
        null=True,
    )

    github = models.URLField(
        blank=True,
        null=True,
    )

    profile_picture = cloudinary_models.CloudinaryField(
        'image',
        folder='user_profile_pictures',
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'User {self.pk}'

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'Applicant Profiles'


class TechnicalSkill(SkillsBaseModel):
    pass


class OtherSkill(SkillsBaseModel):
    pass


class EducationDetail(models.Model):
    INSTITUTION_MAX_LENGTH = 100
    DEGREE_MAX_LENGTH = 10
    PROGRAM_MAX_LENGTH = 100
    LOCATION_MAX_LENGTH = 65

    DEGREE_TYPES = (
        'PhD',
        'Master\'s Degree',
        'Bachelor\'s Degree',
        'High School Diploma',
        'Middle School Diploma',
        'Elementary School Diploma',
        'Professional Qualification',
    )

    institution = models.CharField(
        max_length=INSTITUTION_MAX_LENGTH,
    )

    program = models.CharField(
        max_length=PROGRAM_MAX_LENGTH,
    )

    degree = models.CharField(
        choices=[(x, x) for x in DEGREE_TYPES],
        max_length=max([len(x) for x in DEGREE_TYPES])
    )

    grade = models.CharField(
        max_length=DEGREE_MAX_LENGTH,
    )

    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )


class WorkExperienceDetail(models.Model):
    ROLE_MAX_LENGTH = 65
    LOCATION_MAX_LENGTH = 65
    COMPANY_MAX_LENGTH = 65

    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
    )

    company = models.CharField(
        max_length=COMPANY_MAX_LENGTH,
    )

    description = models.TextField()

    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )
