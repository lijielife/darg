# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-19 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0065_auto_20170311_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='last_active_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
