from django.conf.urls import include, url

urlpatterns = [
    url(r'^$','login.views.home',),
    url(r'deletelog/$','devops.views.deletelog',name='deletelog'),
    url(r'onliestats/$','devops.views.onlinestats',name='onlinestats'),
    url(r'dns_update/update/$','devops.views.dns_update',name='dns_update'),
    url(r'dns_update/cancel/(?P<ID>\d+)/$','devops.views.dns_cancel',name='dns_cancel'),
    url(r'dns_update/apply/(?P<ID>\d+)/$','devops.views.dns_apply',name='dns_apply'),
    url(r'dns_check/$','devops.views.dns_check',name='dns_check'),
    url(r'proxy_update/update/$','devops.views.proxy_updates',name='proxy_update'),
    url(r'proxy_update/list/$','devops.views.proxy_updatelist',name='proxy_updatelist'),
    url(r'proxy_update/apply/(?P<ID>\d+)/$','devops.views.proxy_apply',name='proxy_apply'),
    url(r'proxy_update/cancel/(?P<ID>\d+)/$','devops.views.proxy_cancel',name='proxy_cancel'),
    url(r'proxy_update/okapply/(?P<ID>\d+)/$','devops.views.proxy_okapply',name='proxy_okapply'),
]
