# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-26 12:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170426_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='delivery_date',
            field=models.DateField(default=datetime.datetime(2017, 4, 26, 12, 36, 54, 977312)),
        ),
    ]