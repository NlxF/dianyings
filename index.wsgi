#coding:utf-8
import sae
import os
import sys

root = os.path.dirname(__file__)

# 第三方包路径
sys.path.insert(0, os.path.join(root, 'site-packages'))

from dianying import wsgi

def application(environ, start_response):
    start_response('200 ok', [('content-type', 'text/plain')])
    return ['Hello, SAE!']

application = sae.create_wsgi_app(wsgi.application)