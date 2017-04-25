from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^plans/$', views.index, name='subscription_plans'),
    url(r'^charge/(?P<plan>[a-zA-Z0-9\-]+)/$', views.charge, name='subscription_charge'),
    url(r'^subscribe/successfully/$', views.subscribe_successfully, name='subscribe_successfully'),
    url(r'^cancel/successfully$', views.unsubscribe_successfully, name='unsubscribe_successfully'),
    url(r'^cancel/$', views.unsubscribe, name='subscription_cancel'),
    url(r'^webhook/$', views.webhook, name='subscription_webhook'),
]
