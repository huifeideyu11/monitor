from django.conf.urls import include, url
from django.contrib import admin
from mn_system import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'monitor_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login),
    url(r'^login_action/$', views.login_action),
    url(r'^home/$', views.home),
    url(r'^manage/$', views.interFaceManage),
    url(r'^interfacelist/$', views.interFaceList),
    url(r'^interfacedetail/$', views.interFace_request_detail),

]
