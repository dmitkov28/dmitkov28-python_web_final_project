from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

UserModel = get_user_model()

class SkillsBaseModel(models.Model):
    NAME_MAX_LENGTH = 100
    LEVEL_MIN_VALUE = 0
    LEVEL_MAX_VALUE = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    level = models.IntegerField(
        validators=(
            MinValueValidator(LEVEL_MIN_VALUE),
            MaxValueValidator(LEVEL_MAX_VALUE),
        )
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        unique_together = ('name', 'user')