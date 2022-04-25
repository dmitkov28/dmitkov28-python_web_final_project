# Generated by Django 4.0.4 on 2022-04-18 10:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('benefits', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('industry', models.CharField(max_length=65)),
                ('employees', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('linkedin_profile', models.URLField(blank=True, null=True)),
                ('company_website', models.URLField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
