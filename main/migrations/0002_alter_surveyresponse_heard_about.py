# Generated by Django 5.1.6 on 2025-02-12 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresponse',
            name='heard_about',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
