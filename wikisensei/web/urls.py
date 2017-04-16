# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^price/$', views.price, name='price'),
    url(r'^help/$', views.help, name='help'),
    url(r'^accounts/profile/$', views.profile, name='account_profile'),
    url(r'^wiki/root/', views.WikiRoot.as_view(), name='wiki_root'),
    url(r'^wiki/(?P<pk>\d+)/update', views.WikiUpdate.as_view(), name='wiki_update'),
    url(r'^wiki/(?P<pk>\d+)/', views.WikiDetail.as_view(), name='wiki_show'),
    url(r'^wiki/create/$', views.WikiCreate.as_view(), name='wiki_create'),
    url(r'^wiki/list/$', views.WikiList.as_view(), name='wiki_list'),
]
