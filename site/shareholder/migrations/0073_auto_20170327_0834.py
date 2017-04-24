# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-27 08:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0072_auto_20170323_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='swift',
            field=models.CharField(blank=True, max_length=14),
        ),
        migrations.AlterField(
            model_name='position',
            name='certificate_invalidation_position',
            field=models.OneToOneField(blank=True, help_text='Zugewiesene Transaktion repr\xe4sentiert den Wechsel von Zertifikatsdepot zu Gesellschaftsdepot.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificate_initial_position', to='shareholder.Position'),
        ),
    ]