#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from django.contrib import admin
from .models import *

# Register your models here.

class InterFace_to_DeveloperAdmin(admin.ModelAdmin):
    list_display = ['interface_name', 'email','phone', 'LatestModifyDate', 'editor']

class InterFace_LoginAdmin(admin.ModelAdmin):
    list_display = ('interface_name', 'request_time', 'result', 'reason', 'return_value', 'abnormal')

class InterFace_SearchAdmin(admin.ModelAdmin):
    list_display = ['interface_name', 'request_time', 'result', 'reason', 'return_value', 'abnormal', 'login_result']

class InterFace_AddShopAdmin(admin.ModelAdmin):
    list_display = ['interface_name', 'request_time', 'result', 'reason', 'return_value', 'abnormal', 'login_result']

class InterFace_SubmitOrderAdmin(admin.ModelAdmin):
    list_display = ['interface_name', 'request_time', 'result', 'reason', 'return_value', 'abnormal', 'login_result']

# 下面操作是通知管理工具为这些模块逐一提供界面
admin.site.register(InterFace_to_Developer, InterFace_to_DeveloperAdmin)
admin.site.register(InterFace_Login, InterFace_LoginAdmin)
admin.site.register(InterFace_Search, InterFace_SearchAdmin)
admin.site.register(InterFace_AddShop, InterFace_AddShopAdmin)
admin.site.register(InterFace_SubmitOrder, InterFace_SubmitOrderAdmin)