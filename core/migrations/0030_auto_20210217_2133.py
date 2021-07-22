# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2021-02-17 21:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20210215_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='long_contents',
            field=models.TextField(blank=True, default=None, max_length=25000, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 17, 21, 33, 28, 132516)),
        ),
    ]