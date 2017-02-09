# devops
--------
##功能:  
  曾写过的一版功能测试平台，可用来参考了解django框架的使用方法！<br>
  功能上大部分需要特殊环境，部分如：第三方独立认证，角色管理，URL限制的的实现方法及通过zabbix api管理监控平台可做相应调整使用<br> 
  各目录功能<br>
     login: 权限认证，角色管理，url权限控制<br>
     devops: 流程管理(代理层,内外dns操作流程,域名查询，上线统计,log清理等功能【需要特殊环境】)<br>
     zabbix: 基于zabbix api与管理平台做了一些整合(如用户添加，资产管理，监控开关等)<br>
     templates: 前端html)<br>
     static: (bootstrap)<br>
     
     
##环境：
     ```系统：centos 6.7
     语言： python 2.7
     框架： Django 1.8
     前端： bootstrap-3.2.0
     zabbix: 3.0```
