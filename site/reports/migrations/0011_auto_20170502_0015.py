# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-02 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_report_report_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_at',
            field=models.DateField(verbose_name='report filter date'),
        ),
    ]
