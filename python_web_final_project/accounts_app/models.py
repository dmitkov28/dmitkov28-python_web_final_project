from django.contrib.auth import models as auth_models
from django.db import models

from python_web_final_project.accounts_app.managers import CustomUserManager


class CustomUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    class Meta:
        verbose_name = 'User'

    email = models.EmailField(
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_company = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


class CustomUserProxyCompany(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class CustomUserProxyApplicant(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'
