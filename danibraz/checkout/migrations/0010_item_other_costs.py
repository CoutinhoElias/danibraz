# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-07 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_auto_20180106_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='other_costs',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10, verbose_name='other costs'),
            preserve_default=False,
        ),
    ]
