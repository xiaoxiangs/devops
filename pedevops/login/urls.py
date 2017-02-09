from django.conf.urls import include, url
urlpatterns = [
    url(r'^$','login.views.login',name='login'),
    url(r'^logout/$','login.views.logout',name='logout'),
    url(r'^admin/$','login.views.userlist',name='userlist'),
    url(r'^userdelete/(?P<ID>\d+)/$','login.views.userdelete',name='userdelete'),
    url(r'^useredit/(?P<ID>\d+)/$','login.views.useredit',name='useredit'),
    url(r'^role/$','login.views.rolelist',name='rolelist'),
    url(r'^roleedit/(?P<ID>\d+)/$','login.views.roleedit',name='roleedit'),
    url(r'permission/list/$','login.views.permissionlist',name='permissionlist'),
    url(r'permission/add/$','login.views.permissionadd',name='permissionadd'),
    url(r'permission/edit/(?P<ID>\d+)/$','login.views.permissionedit',name='permissionedit'),
    url(r'permission/delete/(?P<ID>\d+)/$','login.views.permissiondelete',name='permissiondelete'),
    url(r'permission/deny/$','login.views.permissiondeny',name='permissiondeny'),
]
