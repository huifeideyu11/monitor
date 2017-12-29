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

def interFaceEdit(request, id):
    '''
    返回到接口与开发者的编辑页面
    :param request:
    :return: 返回一个接口与开发者的编辑页面
    '''
    username = request.user.username  # 获取登录网址的账号用户名
    interFaceName = InterFace_to_Developer.objects.get(id = id).interface_name
    email = InterFace_to_Developer.objects.get(id = id).email
    phone = InterFace_to_Developer.objects.get(id=id).phone
    print('接口值是：', email)
    return render(request, 'interFaceEdit.html', {'username':username, 'interFaceName':interFaceName,
                                                  'email':email, 'phone':phone, 'id':id})

def interFaceEditSave(request, id):
    '''
    保存修改后的接口管理数据
    :param request:
    :param id: 被修改数据的id号
    :return: 返回到接口管理列表页
    '''
    email = request.POST.get('email', '')         # 获取修改的接口开发者邮箱,eamil对应的是模板中元素的属性name的值
    phone = request.POST.get('phone', '')  # 获取修改的接口开发者手机号
    itd = InterFace_to_Developer.objects.get(id = id)               # 获取被修改接口的数据
    itd.email = email                           # 更新数据库中接口对应的开发者邮箱
    itd.phone = phone                          # 更新数据库中接口对应的开发者手机
    itd.editor = request.user.username                                         # 更新接口修改者的数据
    itd.save()
    return HttpResponseRedirect('/manage/')     # 重定向，视图函数执行完之后，返回值urlpatterns中/manage/对应的视图函数


def interFaceList(request):
    '''
    接口调用详情列表页
    :param request:
    :return: 返回一个接口列表调用详情展示页面
    '''
    interfacelists = interfacelist.objects.all()                # 获取数据库mn_system_interfacelist表中所有数据
    username = request.user.username                            # 获取的当前访问的用户名
    return render(request, 'interfaceCallDetail.html', {'interfacelists': interfacelists, 'username':username})


def interFace_request_detail(request):
    '''
    接口调用详情展示
    :param request:
    :return: 返回一个接口调用详情展示页面，页面以列表形式呈现
    '''
    pass

