# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-06 09:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170505_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='custom_header_meta',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='custom_script_seo',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='plants',
            name='custom_header_meta',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='plants',
            name='custom_script_seo',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2017, 5, 6, 9, 22, 55, 634349)),
        ),
    ]