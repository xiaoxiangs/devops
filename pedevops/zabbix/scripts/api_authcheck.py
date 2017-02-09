#!/usr/bin/python
#coding: utf-8

import json
import urllib2

class token(object):

    def __init__(self,method='',params=''):
        self.url = 'http://zabbixserver/api_jsonrpc.php'
        self.method = method
        self.params = params
        self.auth = False
        self._login()

    def _login(self):
        params = {'user':'admin','password':'xxxx'}
        auth = self.request_data(method='user.login',params=params)
#        print auth
        if 'result' in auth:
            self.auth = auth['result']
        else:
            print auth

    def request_data(self,method,params):
        post_data = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id' : 1
        }

        if (self.auth and (method not in 'user.login')):
            post_data['auth'] = self.auth

        data = json.dumps(post_data)
        req = urllib2.Request(self.url,data)
        req.add_header('Content-Type','application/json-rpc')
        res = urllib2.urlopen(req)
        res_json = json.loads(res.read())
        return res_json

    def result_data(self):
        if self.method != '' and self.params !='':
            self.result = self.request_data(self.method,self.params)
        else:
            self.result = 'input error .please check!'
        return self.result

#method='host.get'
#params={'outpet':'extend'}
#a= token(method,params)
#print a.result_data()
