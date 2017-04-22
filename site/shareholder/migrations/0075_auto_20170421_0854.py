# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-21 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0074_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='security',
            name='title',
            field=models.CharField(choices=[(b'P', 'Vorzugsaktien'), (b'C', 'Stammaktien'), (b'R', 'Namensaktien'), (b'V', 'Vinkulierte Namensaktien')], default=b'C', max_length=1),
        ),
    ]
