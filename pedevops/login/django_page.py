#!/usr/bin/python
#coding: utf-8

from django.core.paginator import Paginator, InvalidPage

def django_Page(request, list,limit):
    '''
      (1).List:为需要分页的数据（一般为*.objects.all()取出来数据）
      (2).Limit:为每页显示的条数

      2.view需要获取SelfPaginator return的lst，并把lst返回给前端模板
        ex:kwvars = {'lPage':lst,}
        
      3.前端需要for循环lPage也就是lst读取每页内容
        ex:{% for i in lPage %} ... {% endfor %}
        
      4.模板页引入paginator.html
        ex:{% include "common/paginator.html" %}
    '''

    paginator = Paginator(list,int(limit))
    page = request.GET.get('page')
    try:
        lst = paginator.page(page)
    except InvalidPage:
        lst = paginator.page(1)

    return lst

if __name__ == '__main__':
    rLIST = User.objects.all()
    lst = django_Page(request,rLIST,20)
