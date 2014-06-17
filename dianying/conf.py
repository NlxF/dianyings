#coding:utf-8
__author__ = 'ISM'

from nanjing.models import Hot10

# movies = Nanjing.objects.all()
# movie_count = movies.count()
# user_count = MyUser.objects.count()
hot10_week = Hot10.hot10_objects.get_week_hot()
hot10_month = Hot10.hot10_objects.get_month_hot()


# def handle_uploaded_file(f):
#     f_path = settings.MEDIA_ROOT + f.name
#     with open(f_path, 'wb+') as info:
#         for chunk in f.chunks():
#             info.write(chunk)
#     return f