#!/usr/bin/python

import api_authcheck
method='host.get'
#params={"output":['hostid'],'selectGroups':'extend','filter':{'host':['BJCER11-18.opi.com',]}}
params={"output":['hostid',],'selectGroups':['groupid','name'],'selectInterfaces':['interfaces','ip'],'filter':{'status':0}}
b = api_authcheck.token(method,params)
print b.result_data()
