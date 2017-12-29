#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from django.contrib import admin
from .models import *

# Register your models here.

class InterFace_to_DeveloperAdmin(admin.ModelAdmin):
    list_display = ['interface_name', 'email','phone', 'LatestModifyDate', 'editor']

class interfacelistAdmin(admin.ModelAdmin):
    list_display = ('interface_name', 'request_time', 'result', 'reason', 'return_value', 'abnormal')


# 下面操作是通知管理工具为这些模块逐一提供界面
admin.site.register(InterFace_to_Developer, InterFace_to_DeveloperAdmin)
admin.site.register(interfacelist, interfacelistAdmin)
