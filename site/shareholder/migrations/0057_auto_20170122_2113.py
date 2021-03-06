# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-22 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareholder', '0056_auto_20170112_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optiontransaction',
            name='depot_type',
            field=models.CharField(blank=True, choices=[(b'0', 'Zertifikatsdepot'), (b'1', 'Gesellschaftsdepot'), (b'2', 'Sperrdepot')], max_length=1, null=True, verbose_name='In welcher Depotart wird das Wertpapier gespeichert.'),
        ),
        migrations.AlterField(
            model_name='position',
            name='depot_type',
            field=models.CharField(blank=True, choices=[(b'0', 'Zertifikatsdepot'), (b'1', 'Gesellschaftsdepot'), (b'2', 'Sperrdepot')], max_length=1, null=True, verbose_name='In welcher Depotart wird das Wertpapier gespeichert.'),
        ),
        migrations.AlterField(
            model_name='security',
            name='cusip',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\xd6ffentliche Wertpapiernummer aka Valor, WKN, CUSIP: http://bit.ly/2ieXwuK'),
        ),
        migrations.AlterField(
            model_name='security',
            name='title',
            field=models.CharField(choices=[(b'P', 'Vorzugsaktien'), (b'C', 'Stammaktien'), (b'R', 'Namensaktien')], default=b'C', max_length=1),
        ),
    ]
