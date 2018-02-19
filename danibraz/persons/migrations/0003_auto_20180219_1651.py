# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-19 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20180216_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='address1',
        ),
        migrations.AddField(
            model_name='person',
            name='observation',
            field=models.CharField(default='Pessoa sem observação', max_length=100, verbose_name='Observações'),
            preserve_default=False,
        ),
    ]
