# Generated by Django 4.0.4 on 2022-04-28 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants_app', '0014_alter_otherskill_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherskill',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='technicalskill',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]