# coding:utf-8
# Created by PyCharm.
# Author  : nick（飞虎队工作室）
# Wechat  : cai9503
# Shop    : https://shop.zbj.com/6463852/
# Date    : 2021/10/11
# Time    : 20:13
from django.contrib import admin
from django.urls import path
from .views import hotels, rooms

urlpatterns = [
    path('', hotels),
    path('rooms/', rooms),
]
