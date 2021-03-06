# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-14 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import reports.models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_report_generation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=reports.models.get_report_upload_path),
        ),
        migrations.AlterField(
            model_name='report',
            name='generation_time',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='time it took to generate the file in seconds'),
        ),
    ]
