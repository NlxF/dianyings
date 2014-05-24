#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from nanjing.models import Nanjing, Comment, Hot10
import datetime
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


def index(request):
    """首页"""
    movie_list = []

    movies = Nanjing.objects.all()
    for m in movies:
        movie_list.append([m, m.tags.all(), m.zone, m.starring.all()])
    return render_to_response(
        "index.html",
        {
            "title": "首页",
            "movies": movie_list,
            "user": request.user,
            'movies_week':  Hot10.hot10_objects.get_week_hot(),
            'movies_month': Hot10.hot10_objects.get_month_hot(),
        },
        context_instance=RequestContext(request)
    )


def latest(request):
    """当用户点击‘最新’时"""
    movie_list = []
    latest_ = Nanjing.objects.order_by('-create_time')
    for m in latest_:
        movie_list.append([m, m.tags.all(), m.zone, m.starring.all()])
    return render_to_response(
        "index.html",
        {
        'title': "最新电影",
        'movies': movie_list,
        'user': request.user,
        'movies_week':  Hot10.hot10_objects.get_week_hot(),
        'movies_month': Hot10.hot10_objects.get_month_hot(),
        },
        context_instance=RequestContext(request)
    )


def sort_by(request, movie_type):
    """当用户点击‘按评分’时"""
    movie_list = []
    if movie_type == 'IMDB':
        title = 'IMDB评分'
        movies = Nanjing.objects.order_by('-score2')
    else:
        title = '豆瓣评分'
        movies = Nanjing.objects.order_by('-score1')
    for m in movies:
        movie_list.append([m, m.tags.all(), m.zone, m.starring.all()])
    return render_to_response(
        "index.html",
        {
        'title': title,
        'movies': movie_list,
        'user': request.user,
        'movies_week': Hot10.hot10_objects.get_week_hot(),
        'movies_month': Hot10.hot10_objects.get_month_hot(),
        },
        context_instance=RequestContext(request)
    )


def zone(request, movie_zone):
    """当用户点击“地区”时"""
    movie_list = []
    if movie_zone == 'dalu':
        title = u'大陆电影'
        filter_type = Q(zone__zone='大陆')|Q(zone__zone='中国大陆')
    elif movie_zone == 'gangaotai':
        title = u'港澳台电影'
        filter_type = Q(zone__zone='香港')| Q(zone__zone='台湾')| Q(zone__zone='澳门')
    elif movie_zone == 'oumei':
        title = u'欧美电影'
        filter_type = Q(zone__zone='美国')|Q(zone__zone='英国')|Q(zone__zone='德国')|Q(zone__zone='法国')
    elif movie_zone == 'rihan':
        title = u'日韩电影'
        filter_type = Q(zone__zone='日本')|Q(zone__zone='韩国')
    elif movie_zone == 'qita':
        title = u'其他电影'
        filter_type = ~(Q(zone__zone='中国大陆')|Q(zone__zone='香港')|
                        Q(zone__zone='台湾')|Q(zone__zone='澳门')|
                        Q(zone__zone='美国')|Q(zone__zone='英国')|
                        Q(zone__zone='德国')|Q(zone__zone='法国')|
                        Q(zone__zone='日本')|Q(zone__zone='韩国'))
    else:
        title = movie_zone
        filter_type = Q(zone__zone=movie_zone)
    movies = Nanjing.objects.filter(filter_type)
    for m in movies:
        movie_list.append([m, m.tags.all(), m.zone, m.starring.all()])
    return render_to_response(
        "index.html",
        {
        'title': title,
        'movies': movie_list,
        'user': request.user,
        'movies_week': Hot10.hot10_objects.get_week_hot(),
        'movies_month': Hot10.hot10_objects.get_month_hot(),
        },
        context_instance=RequestContext(request)
    )


def movie_tag(request, tag):
    """通过标签分类"""
    movie_list = []
    try:
        title = tag+u'电影'
        movies = Nanjing.objects.filter(tags__type=tag)
    except Nanjing.DoesNotExist:
        return render_to_response('error.html', {"error_message": tag+u"类型电影还不存在，请过段时间再试试~"},
                                  context_instance=RequestContext(request))
    for m in movies:
        movie_list.append([m, m.tags.all(), m.zone, m.starring.all()])
    return render_to_response(
        "index.html",
        {
        'title': title,
        'movies': movie_list,
        'user': request.user,
        'movies_week': Hot10.hot10_objects.get_week_hot(),
        'movies_month': Hot10.hot10_objects.get_month_hot(),
        },
        context_instance=RequestContext(request)
    )


def by_name(request, name):
    """通过名字分类"""
    movie_list = []
    try:
        title = name+u'电影'
        movies1 = Nanjing.objects.filter(starring__name=name)
    except Nanjing.DoesNotExist:
        pass
    try:
        movies2 = Nanjing.objects.filter(director__name=name)
    except Nanjing.DoesNotExist:
        pass
    if movies1 and movies2:
        movies = movies1 + movies2
    elif movies1:
        movies = movies1
    elif movies2:
        movies = movies2
    else:
        return render_to_response('error.html', {"error_message": name+u"的电影还不存在，请过段时间再试试~"}, context_instance=RequestContext(request))
    for m in movies:
        movie_list.append([m, m.tags.all(), m.zone, m.starring.all()])
    return render_to_response(
        "index.html",
        {
        'title': title,
        'movies': movie_list,
        'user': request.user,
        'movies_week': Hot10.hot10_objects.get_week_hot(),
        'movies_month': Hot10.hot10_objects.get_month_hot(),
        },
        context_instance=RequestContext(request)
    )


def movie_id(request, movie_id_):
    """当用户通过右侧的排行榜来查看影片信息"""
    try:
        movie = Nanjing.objects.get(id=int(movie_id_))
    except Nanjing.DoesNotExist:
        return render_to_response('error.html', {"error_message": "电影还不存在，请过段时间再试试~"},
                                  context_instance=RequestContext(request))
    if movie:
        movie.click += 1
        movie.save()
        hot = Hot10.objects.get(movie=movie)
        hot.today += 1
        hot.save()
        comments = movie.movie_comment.all()
        download_links = movie.download.all()
        pic = movie.image_upload.split(',')
        return render_to_response(
            'a-movie.html',
            {
                'title': movie.title,
                'user': request.user if request.user.is_authenticated() else None,
                'movie': movie,
                'pictures': pic,
                'links': download_links,
                'comments': comments,
                'movies_week': Hot10.hot10_objects.get_week_hot(),
                'movies_month': Hot10.hot10_objects.get_month_hot(),
            },
            context_instance=RequestContext(request)
        )


def create_reply(request, movie_id_):
    """创建回复"""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        try:
            movie = Nanjing.objects.get(id=int(movie_id_))
        except Nanjing.DoesNotExist:
            return render_to_response('error.html',
                                      {"error_message": "电影还不存在，请过段时间再试试~"},
                                      context_instance=RequestContext(request)
            )
        comments = movie.movie_comment.all()
        download_links = movie.download.all()
        movie.reply_count += 1
        movie.click += 1
        new_comment = Comment(text=content, data=datetime.datetime.now())
        new_comment.nanjing = movie
        new_comment.username = request.user
        #必须调用save函数写入数据库后才能添加一对多，否则comment对象在数据库中没有对应primary_key
        new_comment.save()
        # 保存外键关系
        request.user.user.add(new_comment)
        movie.movie_comment.add(new_comment)
        movie.save()
        return HttpResponseRedirect(reverse("nj:movie", args=(movie.id,)))