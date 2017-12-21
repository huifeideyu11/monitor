#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from django.db import models
from django.utils import timezone

# Create your models here.

# 接口和开发者对应关系表
class InterFace_to_Developer(models.Model):
    interface_name = models.CharField(max_length=200)           # 接口
    developerName = models.CharField(max_length=200)           # 开发人员姓名
    LatestModifyDate = models.DateTimeField(auto_now=True)     # 获取更新表格的时间
    editor = models.CharField(max_length=200)                   # 表数据修改者即用户登录名

    def __str__(self):                                     # 设置调用该类时，实例默认显示的对象
        return self.interface

class InterFace_Login(models.Model):
    interface_name = models.CharField(default='登录接口', max_length=200)    # 接口名称， 登录接口
    request_time = models.DateTimeField(auto_now=True)     # 接口调用时间
    result = models.CharField(max_length=100)               # 接口调用结果（值只有：success和fail）
    reason = models.CharField(max_length=200)               # 原因分为：接口调用异常和接口返回值错误
    return_value = models.CharField(max_length=200)         # 接口返回值错误时，接口的返回值
    abnormal = models.CharField(max_length=200)             # 接口访问异常时，异常信息

    def __str__(self):
        return self.interface_name

class InterFace_Search(models.Model):
    interface_name = models.CharField(default='搜索接口', max_length=200)  # 接口名称， 搜索接口
    login_result = models.CharField(max_length=100)  # 登录情况（值只有：success和fail）
    request_time = models.DateTimeField(auto_now=True)  # 若登录失败，接口调用时间为调登录接口失败的时间
    result = models.CharField(max_length=100)  # 接口调用结果（值只有：success和fail）
    reason = models.CharField(max_length=200)  # 原因分为：接口调用异常和接口返回值错误
    return_value = models.CharField(max_length=200)  # 接口返回值错误时，接口的返回值
    abnormal = models.CharField(max_length=200)  # 接口访问异常时，异常信息

    def __str__(self):
        return self.interface_name

class InterFace_AddShop(models.Model):
    interface_name = models.CharField(default='添加购物车', max_length=200)  # 接口名称， 添加购物车接口
    login_result = models.CharField(max_length=100)  # 登录情况（值只有：success和fail）
    request_time = models.DateTimeField(auto_now=True)  # 若登录失败，接口调用时间为调登录接口失败的时间
    result = models.CharField(max_length=100)  # 接口调用结果（值只有：success和fail）
    reason = models.CharField(max_length=200)  # 原因分为：接口调用异常和接口返回值错误
    return_value = models.CharField(max_length=200)  # 接口返回值错误时，接口的返回值
    abnormal = models.CharField(max_length=200)  # 接口访问异常时，异常信息

    def __str__(self):
        return self.interface_name

class InterFace_SubmitOrder(models.Model):
    interface_name = models.CharField(default='提交订单接口', max_length=200)  # 接口名称， 提交订单接口
    login_result = models.CharField(max_length=100)  # 登录情况（值只有：success和fail）
    request_time = models.DateTimeField(auto_now=True)  # 若登录失败，接口调用时间为调登录接口失败的时间
    result = models.CharField(max_length=100)  # 接口调用结果（值只有：success和fail）
    reason = models.CharField(max_length=200)  # 原因分为：接口调用异常和接口返回值错误
    return_value = models.CharField(max_length=200)  # 接口返回值错误时，接口的返回值
    abnormal = models.CharField(max_length=200)  # 接口访问异常时，异常信息

    def __str__(self):
        return self.interface_name



