# Generated by Django 4.0.4 on 2022-04-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants_app', '0011_remove_applicantprofile_looking_for_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherskill',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='technicalskill',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
