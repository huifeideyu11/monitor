from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

# Create your views here.

def login(request):
    '''
        登录页面
    :param request:
    :return:返回一个登录页面
    '''
    return render(request, 'login.html')

def login_action(request):    # 登录视图
    '''
    登录页面执行登录时，进行用户名校验
    '''
    print('提交登录请求')
    if request.method =='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)  #用户登录认证，当用户登录名和密码正确时，返回一个user对象，否则返回一个None
        print(user)
        if user is not None:
            auth.login(request, user) #登录
            request.session['user'] = username  # 将session信息记录到浏览器
            # response.set_cookie('user', username, 3600)  #添加浏览器cookie
            response = HttpResponseRedirect('/home/')   # 重定向，登录成功后指向/home/路径
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error!'})

def home(request):
    '''
    视图返回网站主页
    :param request:
    :return:
    '''
    username = request.user.username    # 获取登录网址的账号用户名
    return render(request, 'home1.html', {'username':username})

def interFaceManage(request):
    '''
    视图返回：接口与相应的开发者对应关系列表页
    :param request:
    :return:
    '''
    username = request.user.username    # 获取登录网址的账号用户名
    InterFace_to_Developers = InterFace_to_Developer.objects.all()    # 获取数据库中InterFace_to_Developer表中所有数据
    return render(request, 'interfaceManage1.html', {'InterFace_to_Developers': InterFace_to_Developers, 'username':username})

def interFaceList(request):
    '''
    接口列表
    :param request:
    :return: 返回一个接口列表展示页面，点击相应接口可以查看接口的调用详情
    '''
    pass

def interFace_request_detail(request):
    '''
    接口调用详情展示
    :param request:
    :return: 返回一个接口调用详情展示页面，页面以列表形式呈现
    '''
    pass