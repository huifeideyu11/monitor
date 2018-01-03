#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from django.db import models
from django.utils import timezone

# Create your models here.

# 接口和开发者对应关系表
class InterFace_to_Developer(models.Model):
    interface_name = models.CharField(max_length=200, verbose_name='接口名称')           # 接口
    email = models.CharField(max_length=200, verbose_name='邮箱')        # 邮件报警通知人员的邮箱地址
    phone = models.CharField(max_length=200, verbose_name='手机号')      # 短信报警人员的手机号
    LatestModifyDate = models.DateTimeField(auto_now=True, verbose_name='更新时间')     # 获取更新表格的时间
    editor = models.CharField(max_length=200, verbose_name='修改者')                   # 表数据修改者即用户登录名

    def __str__(self):                                     # 设置调用该类时，实例默认显示的对象
        return self.interface_name    # 注意：只能返回字符串


class interfacelist(models.Model):
    '''
    用于存储各列表被调用的详情
    '''
    interface_name = models.CharField(max_length=200)  # 接口名称， 添加购物车接口
    login_result = models.CharField(max_length=100)  # 登录情况（值只有：success和fail）
    request_time = models.DateTimeField(auto_now=True)  # 若登录失败，接口调用时间为调登录接口失败的时间
    result = models.CharField(max_length=100, blank=True, null=True)  # 接口调用结果（值只有：success和fail）
    reason = models.CharField(max_length=200, blank=True, null=True)  # 原因分为：接口调用异常和接口返回值错误
    return_value = models.CharField(max_length=200, blank=True, null=True)  # 接口返回值错误时，接口的返回值
    abnormal = models.TextField(blank=True, null=True)  # 接口访问异常时，异常信息

    def __str__(self):
        return self.interface_name
