# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-09 20:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_item_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='total',
        ),
    ]
