# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-10 08:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0052_remove_userprofile_pobox_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nationality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nationality', to='shareholder.Country'),
        ),
    ]