#coding:utf-8
__author__ = 'ISM'
from django.conf import settings
from MyUser.models import MyUser
from nanjing.models import Nanjing, Hot10

# movies = Nanjing.objects.all()
# movie_count = movies.count()
# user_count = MyUser.objects.count()
# hot10_week = Hot10.hot10_objects.get_week_hot()
# hot10_mouth = Hot10.hot10_objects.get_mouth_hot()


def handle_uploaded_file(f):
    f_path = settings.MEDIA_ROOT + f.name
    with open(f_path, 'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
    return f