# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-12 17:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0012_remove_item_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papel', to='checkout.Papel'),
        ),
    ]
