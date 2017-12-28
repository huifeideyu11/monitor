from django.conf.urls import include, url
from django.contrib import admin
from mn_system import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'monitor_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),                    # 后台管理页面
    url(r'^login/$', views.login),                                # 登录页面链接
    url(r'^login_action/$', views.login_action),                 # 执行登录操作
    url(r'^home/$', views.home),                                   # 主页
    # -- 接口管理 -- #
    url(r'^manage/$', views.interFaceManage),                     # 接口管理列表页链接
    url(r'^manage/edit/(\d+)$', views.interFaceEdit),            # 接口管理编辑页面链接
    url(r'^manage/edit/(\d+)/save/$', views.interFaceEditSave),  # 保存接口管理修改的数据

    # -- 接口调用 -- #
    url(r'^interfacelist/$', views.interFaceList),
    url(r'^interfacedetail/$', views.interFace_request_detail),
]


