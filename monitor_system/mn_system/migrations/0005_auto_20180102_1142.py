# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-02 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mn_system', '0004_delete_developer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interfacelist',
            name='abnormal',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='interfacelist',
            name='reason',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='interfacelist',
            name='result',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='interfacelist',
            name='return_value',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]