# Generated by Django 4.0.4 on 2022-04-23 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies_app', '0004_alter_companyprofile_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyprofile',
            old_name='profile_picture',
            new_name='logo',
        ),
    ]
