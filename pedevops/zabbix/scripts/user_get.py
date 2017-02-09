#!/usr/bin/python

import api_authcheck
method='user.get'
#params={"output":['hostid'],'selectGroups':'extend','filter':{'host':['BJCER11-18.opi.com',]}}
params={"output":['userid','alias','permission','type'],'userids':'3','selectMedias':['sendto','period'],'selectUsrgrps':['name','users_status'],'sortfield':'alias'}
b = api_authcheck.token(method,params)
#print b.result_data()

for i in b.result_data()['result']:
  print i
