# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-22 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0067_userprofile_is_multi_company_allowed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=60)),
                ('postal_code', models.CharField(blank=True, max_length=10)),
                ('street', models.CharField(blank=True, max_length=35)),
                ('city', models.CharField(blank=True, max_length=35)),
                ('swift', models.CharField(max_length=14)),
                ('bcnr', models.CharField(max_length=5)),
                ('branchid', models.CharField(max_length=4)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Banks',
            },
        ),
        migrations.AlterModelOptions(
            name='operator',
            options={'ordering': ['company__name']},
        ),
    ]
