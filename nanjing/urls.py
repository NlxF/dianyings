#coding:utf-8
__author__ = 'ISM'

from django.conf.urls import url, patterns, include

urlpatterns = patterns('nanjing.views',
    url(r'^$', 'index', name='index'),
    url(r'^index/$', 'index'),
    url(r'^latest/$', "latest", name='latest'),
    url(r'^sort/(?P<movie_type>\w{4,6})/$', 'sort_by', name='sort'),
    url(r'^zone/(?P<movie_zone>\w{1,9})/$', 'zone', name='zone'),
    url(r'^tags/(?P<tag>.*)/$', "movie_tag", name='tags'),
    url(r'^name/(?P<name>.*)/$', 'by_name', name='name'),
    url(r'^movie/(?P<movie_id_>\d+)/$', 'movie_id', name='movie'),
    url(r'^create_reply/(?P<movie_id_>\d+)$', 'create_reply', name='create_reply'),
)