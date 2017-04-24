# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='site_index'),
    url(r'^home/', views.WikiRoot.as_view(), name='home'),
    url(r'^home/', views.WikiRoot.as_view(), name='wiki_root'),
    url(r'^price/$', views.Price.as_view(), name='price'),
    url(r'^help/$', views.Help.as_view(), name='help'),
    url(r'^accounts/profile/$', views.Profile.as_view(), name='account_profile'),
    url(r'^accounts/custom_style/$', views.CustomStyle.as_view(), name='account_custom_style'),
    url(r'^wiki/(?P<pk>\d+)/update', views.WikiUpdate.as_view(), name='wiki_update'),
    url(r'^wiki/(?P<pk>\d+)/revisions/(?P<version>\d+)', views.WikiRevision.as_view(), name='wiki_revision'),
    url(r'^wiki/(?P<pk>\d+)/', views.WikiDetail.as_view(), name='wiki_show'),
    url(r'^wiki/(?P<username>\w+)/home', views.UserWikiHome.as_view(), name='user_wiki_home'),
    url(r'^wiki/create/$', views.WikiCreate.as_view(), name='wiki_create'),
    url(r'^wiki/list/$', views.WikiList.as_view(), name='wiki_list'),
]
