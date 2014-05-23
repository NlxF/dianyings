#coding:utf-8
from django import forms
from django.db import models
from django.contrib import admin
from nanjing.models import AllActors, AllType, AllZone, Comment, Nanjing, Links, Director, Hot10


class CommentAdmin(admin.ModelAdmin):
    pass


class NanjingAdmin(admin.ModelAdmin):
    exclude = ("reply_count", "click")


admin.site.register(AllActors)
admin.site.register(AllZone)
admin.site.register(AllType)
admin.site.register(Links)
admin.site.register(Director)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Nanjing, NanjingAdmin)