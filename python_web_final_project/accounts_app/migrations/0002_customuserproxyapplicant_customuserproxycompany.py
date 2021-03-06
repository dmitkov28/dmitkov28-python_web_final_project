# Generated by Django 4.0.4 on 2022-04-27 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserProxyApplicant',
            fields=[
            ],
            options={
                'verbose_name': 'Applicant',
                'verbose_name_plural': 'Applicants',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts_app.customuser',),
        ),
        migrations.CreateModel(
            name='CustomUserProxyCompany',
            fields=[
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts_app.customuser',),
        ),
    ]
