from cloudinary import models as cloudinary_models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

UserModel = get_user_model()


class CompanyProfile(models.Model):
    COMPANY_NAME_MAX_LENGTH = 50
    ADDRESS_MAX_LENGTH = 255
    INDUSTRY_MAX_LENGTH = 65
    PHONE_MAX_LENGTH = 13
    USER_IS_NOT_COMPANY_MESSAGE = 'User must be a company.'

    name = models.CharField(
        max_length=COMPANY_NAME_MAX_LENGTH,
        null=True,
        blank=True,
        unique=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    benefits = models.TextField(
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        null=True,
        blank=True,
    )

    industry = models.CharField(
        null=True,
        blank=True,
        max_length=INDUSTRY_MAX_LENGTH,
    )

    employees = models.IntegerField(
        null=True,
        blank=True,
        validators=(
            MinValueValidator(0),
        )
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

    company_website = models.URLField(
        blank=True,
        null=True,
    )

    logo = cloudinary_models.CloudinaryField(
        null=True,
        blank=True,
        folder='company_logos',
    )

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,

    )

    def clean(self):
        if not self.user.is_company:
            raise ValidationError(self.USER_IS_NOT_COMPANY_MESSAGE)

    def __str__(self):
        return self.name if self.name else 'Unknown'
