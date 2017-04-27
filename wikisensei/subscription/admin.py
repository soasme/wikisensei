# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Customer, Subscription, SubscriptionEvent, WebhookEvent

class CustomerAdmin(admin.ModelAdmin):
    pass

class SubscriptionAdmin(admin.ModelAdmin):
    pass

class SubscriptionEventAdmin(admin.ModelAdmin):
    pass

class WebhookEventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionEvent, SubscriptionEventAdmin)
admin.site.register(WebhookEvent, WebhookEventAdmin)
