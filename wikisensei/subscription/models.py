# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class AnnualPlan(object):
    id = 'tomato-annual'
    name = 'Tomato Annual Plan'
    description = 'The annual subscription plan to Tomato ($19.99).'
    price = 1999 # $19.99
    currency = 'usd'
    interval = 'month'
    image = '/static/images/subscription/pro-annual.png'

class MonthlyPlan(object):
    id = 'tomato-monthly'
    name = 'Tomato Monthly Plan'
    description = 'The monthly subscription plan to Tomato ($1.99).'
    price = 199 # $1.99
    currency = 'usd'
    interval = 'month'
    image = '/static/images/subscription/pro-monthly.png'

class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

class SubscriptionEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class WebhookEvent(models.Model):
    stripe_id = models.CharField(max_length=64, unique=True)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
