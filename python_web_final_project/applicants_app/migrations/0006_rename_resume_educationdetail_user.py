# Generated by Django 4.0.4 on 2022-04-19 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicants_app', '0005_educationdetail_program'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educationdetail',
            old_name='resume',
            new_name='user',
        ),
    ]
