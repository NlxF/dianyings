#coding:utf-8
from django.db import models
from django.conf import settings


class AllActors(models.Model):
    name = models.CharField(max_length=50, verbose_name="演员名")

    class Meta:
        db_table = 'all_actors'
        verbose_name_plural = '演员'

    def __unicode__(self):
        return self.name


class AllType(models.Model):
    """movie type"""
    type = models.CharField(max_length=20, verbose_name='电影类型')

    class Meta:
        db_table = 'alltype'
        verbose_name_plural = '类型'

    def __unicode__(self):
        return self.type


class AllZone(models.Model):
    zone = models.CharField(max_length=20, verbose_name='地区')

    class Meta:
        db_table = 'allzone'
        verbose_name_plural = '地区'

    def __unicode__(self):
        return self.zone


class Director(models.Model):
    name = models.CharField(max_length=50, verbose_name='导演')

    class Meta:
        db_table = 'director'
        verbose_name_plural = "导演"

    def __unicode__(self):
        return self.name


class Nanjing(models.Model):
    """movie's info"""
    title = models.CharField(max_length=255, db_index=True, verbose_name=u"电影名")
    director = models.ForeignKey(Director, related_name="directors", verbose_name=u'导演')
    starring = models.ManyToManyField(AllActors, related_name="actors", verbose_name=u"主演")
    tags = models.ManyToManyField(AllType, related_name="movie_tags", verbose_name=u"类型")
    zone = models.ForeignKey(AllZone, related_name="movie_zone", verbose_name=u"地区")
    #image_upload = models.ImageField(blank=True, null=True, upload_to='movies/images', verbose_name=u'剧照')
    image_upload = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'剧照')
    image_search = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"海报")
    showtime = models.CharField(max_length=80, verbose_name=u"上映时间")
    movie_time = models.CharField(max_length=100, verbose_name=u"时长")
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    score1 = models.FloatField(verbose_name=u"豆瓣", db_index=True)
    score2 = models.FloatField(verbose_name='IMDB', db_index=True)
    summary = models.TextField(verbose_name=u"简介")
    reply_count = models.IntegerField(default=0, verbose_name=u'评论次数')
    click = models.IntegerField(default=0, verbose_name=u'点击次数')

    class Meta:
        db_table = 'movie'
        verbose_name_plural = u'电影'

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Nanjing, self).save()
        Hot10.objects.get_or_create(movie=self)

    # @models.permalink
    # def get_absolute_url(self):
    #     return ('nanjing.views.movie_id', [str(self.id)])


class Comment(models.Model):
    """movie's comment"""
    username = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', verbose_name=u"用户名")
    text = models.TextField(verbose_name=u"评论内容")
    data = models.DateTimeField(verbose_name=u"评论时间")
    nanjing = models.ForeignKey(Nanjing, related_name='movie_comment', verbose_name=u'电影')

    class Meta:
        db_table = 'comment'
        verbose_name_plural = u'评论'

    def __unicode__(self):
        return self.nanjing.title


class Links(models.Model):
    link = models.CharField(max_length=900, verbose_name=u'下载链接')
    size = models.CharField(max_length=50,  verbose_name=u'资源大小')
    #aiqiyi = models.CharField(max_length=200, verbose_name=u'爱奇艺')
    nanjing = models.ForeignKey(Nanjing, related_name='download', verbose_name=u'电影')

    class Meta:
        db_table = 'links'
        verbose_name_plural = u'链接'

    def __unicode__(self):
        return self.link


class Hot10Manager(models.Manager):
    def get_order_by(self, weekly_monthly):
        by_xxx = super(Hot10Manager, self).get_queryset().order_by(weekly_monthly)
        if by_xxx.count() > 10:
            by_xxx = by_xxx[:10]
        return by_xxx

    def get_week_hot(self):
        return self.get_order_by('-week')

    def get_month_hot(self):
        return self.get_order_by('-month')


class Hot10(models.Model):
    movie = models.OneToOneField(Nanjing, related_name="movie")
    creation = models.DateField(auto_now_add=True)
    today = models.PositiveIntegerField(default=0)
    weekly_click = models.CommaSeparatedIntegerField(max_length=300, default='0,0,0,0,0,0,0')
    monthly_click = models.CommaSeparatedIntegerField(
        max_length=1000,
        default='0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
    )
    week = models.PositiveIntegerField(default=0, db_index=True)
    month = models.PositiveIntegerField(default=0, db_index=True)
    is_changed = models.BooleanField(default=False)

    objects = models.Manager()
    hot10_objects = Hot10Manager()

    class Meta:
        db_table = 'hot'
        verbose_name_plural = u"排行榜"

    def __unicode__(self):
        return u"排行榜"


# weekly_hot = None
# monthly_hot = None


# from apscheduler.scheduler import Scheduler
# import logging
# logging.basicConfig()
# __MYSQL_url = 'mysql://root:toor@localhost/w'
# __configure = {
#     'apscheduler.standalone':True,
#     'apscheduler.jobstores.sqlalchemy_store.class': 'apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore',
#     'apscheduler.jobstores.sqlalchemy_store.url': __MYSQL_url
# }
#
# scheduler = Scheduler()


#@scheduler.cron_schedule(second='1', minute='12', hour='2-3', day_of_week='0-6')
# def updatehot10everynanjing():
#     """更新排行榜 在2:12:1"""
#     import datetime
#     today = datetime.date.today()
#     movies = Hot10.objects.all()
#     for m in movies:
#         """index1是每周排行榜，index2是每月排行榜"""
#         index1 = abs((today-m.creation).days) % 7
#         index2 = abs((today-m.creation).days) % 30
#         weekly_click = m.weekly_click.split(',')
#         monthly_click = m.monthly_click.split(',')
#         weekly_click[index1-1] = str(m.today)
#         monthly_click[index2-1] = str(m.today)
#         m.weekly_click = ','.join(weekly_click)
#         m.monthly_click = ','.join(monthly_click)
#         m.week = sum(int(x) for x in weekly_click)
#         m.month = sum(int(x) for x in monthly_click)
#         m.today = 0
#         m.save()
    # global weekly_hot
    # global monthly_hot
    # weekly_hot = Hot10.hot10_objects.get_week_hot()
    # monthly_hot = Hot10.hot10_objects.get_month_hot()

#scheduler.start()
