#coding:utf-8
__author__ = 'ISM'

from django.conf.urls import url, patterns, include

urlpatterns = patterns("MyUser.views",
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', 'login', name='login'),
    url(r'^setting/$', 'setting', name='setting'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        "reset_confirm", name='reset_confirm'),
    url(r'rest/passwd/$', 'reset_password', name='reset_password')
)