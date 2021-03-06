# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-23 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0057_auto_20170122_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='vote_ratio',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Voting rights calculation: one vote per X of security.face_value'),
        ),
    ]
