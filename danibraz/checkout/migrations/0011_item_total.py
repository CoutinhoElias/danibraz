# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-07 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_item_other_costs'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='total',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10, verbose_name='total'),
            preserve_default=False,
        ),
    ]
