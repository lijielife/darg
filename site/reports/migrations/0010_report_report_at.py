# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-01 23:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_auto_20170415_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_at',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2017, 5, 1, 23, 49, 26, 530614, tzinfo=utc)),
            preserve_default=False,
        ),
    ]