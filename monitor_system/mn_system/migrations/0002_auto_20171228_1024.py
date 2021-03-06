# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-12-28 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mn_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interface_to_developer',
            name='developerName',
        ),
        migrations.AddField(
            model_name='interface_to_developer',
            name='email',
            field=models.CharField(default='631442624@qq.com', max_length=200, verbose_name='邮箱'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interface_to_developer',
            name='phone',
            field=models.CharField(default='13694917391', max_length=200, verbose_name='手机号'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='interface_to_developer',
            name='LatestModifyDate',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='interface_to_developer',
            name='editor',
            field=models.CharField(max_length=200, verbose_name='修改者'),
        ),
        migrations.AlterField(
            model_name='interface_to_developer',
            name='interface_name',
            field=models.CharField(max_length=200, verbose_name='接口名称'),
        ),
    ]
