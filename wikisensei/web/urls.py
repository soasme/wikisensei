# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^accounts/profile/$', views.profile, name='account_profile'),
    url(r'^wiki/(?P<username>[\w\d]+)/(?P<title>[^/]+)/', views.show_wiki, name='show_wiki'),
]
