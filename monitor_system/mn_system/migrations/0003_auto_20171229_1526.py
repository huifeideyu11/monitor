# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-12-29 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mn_system', '0002_auto_20171228_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='interfaceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface_name', models.CharField(max_length=200)),
                ('login_result', models.CharField(max_length=100)),
                ('request_time', models.DateTimeField(auto_now=True)),
                ('result', models.CharField(max_length=100)),
                ('reason', models.CharField(max_length=200)),
                ('return_value', models.CharField(max_length=200)),
                ('abnormal', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='InterFace_AddShop',
        ),
        migrations.DeleteModel(
            name='InterFace_Login',
        ),
        migrations.DeleteModel(
            name='InterFace_Search',
        ),
        migrations.DeleteModel(
            name='InterFace_SubmitOrder',
        ),
    ]