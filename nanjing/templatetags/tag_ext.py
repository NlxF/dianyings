#coding:utf-8
__author__ = 'ISM'
from django import template
import urllib

register = template.Library()


@register.filter(name='sp')
def specific_information(value):
    if value and value.startswith('magnet:?'):
        #去掉首位 只留中间
        if value.find('&tr=') > 0:
            value = value[value.find('dn=')+3:value.find('&tr=')].encode()
        else:
            value = value[value.find('dn=')+3:].encode()
        value = urllib.unquote(value)
        return value


