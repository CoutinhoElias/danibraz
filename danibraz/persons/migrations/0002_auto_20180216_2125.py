# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-17 00:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='kynd',
            new_name='kind',
        ),
        migrations.AlterField(
            model_name='address',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='persons.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('person', 'kind')]),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
