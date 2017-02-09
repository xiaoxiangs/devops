#!/usr/bin/python

import api_authcheck
method='usergroup.get'
#params={"output":['hostid'],'selectGroups':'extend','filter':{'host':['BJCER11-18.opi.com',]}}
#params={"output":['userid','alias'],'selectMedias':['sendto','period'],'selectUsrgrps':'extend'}
params={'output':['usrgrpid','name']}
b = api_authcheck.token(method,params)
print b.result_data()['result']
#for i in b.result_data()['result']:
#  print i
