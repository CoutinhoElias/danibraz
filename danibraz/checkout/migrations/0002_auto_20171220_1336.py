# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-20 16:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('transaction_kind', models.CharField(choices=[('in', 'Entrada'), ('out', 'Saida'), ('eaj', 'Entrada de Ajuste'), ('saj', 'Saída de Ajuste')], max_length=4)),
                ('date_transaction', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='checkout.Product')),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.PositiveSmallIntegerField(verbose_name='quantidade'),
        ),
    ]
