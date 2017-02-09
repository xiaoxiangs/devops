from django.conf.urls import include, url

urlpatterns = [
#    url(r'list/$','zabbix.views.list',name='monitor_list'),
#    url(r'list/(?P<ID>\d+)/$','zabbix.views.operation',name='host_operation'),
    url(r'^hostlist/(?P<ID>\d+)/$','zabbix.views.list',name='monitor_list'),
    url(r'^hostlist/(?P<groupid>\d+)/(?P<hostid>\d+)/$','zabbix.views.operation',name='host_operation'),
    url(r'^userlist/(?P<sID>\d+)/$','zabbix.views.userlist',name='user_list'),
    url(r'^userlist/(?P<usergroupid>\d+)/(?P<userid>\d+)/$','zabbix.views.userdel',name='user_del'),
    url(r'^userlist/useredit/(?P<userID>\d+)/$','zabbix.views.monitoruseredit',name='monitoruser_edit'),
    url(r'^userlist/useradd/$','zabbix.views.useradd',name='monitor_useradd'),
]
