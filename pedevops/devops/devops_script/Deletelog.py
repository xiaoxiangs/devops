#!/usr/local/bin/python
import sys
import os
import paramiko
import gssapi
import datetime


def del_log(host,cmd,function):
    requs = {'code':0}
#    Authen = os.popen('klist')
#    kauthen = Authen.read()
#    if kauthen.find('xiang.xiao3@XIAONEI.OPI.COM') == -1:
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.load_system_host_keys()
    try:
        conn.connect(host,22,username='web',gss_auth=True,gss_kex = True ,gss_deleg_creds = True,timeout=60)
    except:
        os.system("kinit xiang.xiao3 <<EOF\xxxxx\nEOF")
        conn.connect(host,22,username='web',gss_auth=True,gss_kex = True ,gss_deleg_creds = True,timeout=60)
    stdin, stdout, stderr = conn.exec_command(cmd, timeout=300)
    commd_out = stdout.read()
    error_out = stderr.read()
    conn.close()
    if len(error_out) != 0:
        requs['code'] = 1
    log_record = '\ncommd_out:%s\nerror_out:%s' % (commd_out,error_out)
#    requs['log_record'] = log_record
    requs['log_record'] = 'commd_out:%s' % error_out
    requs['commd_out'] = commd_out
    deldate = datetime.datetime.now().strftime('%Y-%m-%d')
    requedata = '%s    %s' %(deldate,str(requs))
    log_file = open('/data/logs/django/%s.log' % function,'a')
    log_file.write(requedata)
    log_file.close()
    print requs
    return requs

if __name__ == '__main__':
    hosts = sys.argv[1]
    cmds = sys.argv[2]
    functions = sys.argv[3]
    del_log(host=hosts,cmd=cmds,function=functions)

