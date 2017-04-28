# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from .models import Customer, Subscription, SubscriptionEvent, WebhookEvent, SubscriptionExemption

class CustomerAdmin(ForeignKeyAutocompleteAdmin):
    pass

class SubscriptionAdmin(ForeignKeyAutocompleteAdmin):
    pass

class SubscriptionEventAdmin(ForeignKeyAutocompleteAdmin):
    pass

class WebhookEventAdmin(ForeignKeyAutocompleteAdmin):
    pass

class SubscriptionExemptionAdmin(ForeignKeyAutocompleteAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionEvent, SubscriptionEventAdmin)
admin.site.register(WebhookEvent, WebhookEventAdmin)
admin.site.register(SubscriptionExemption, SubscriptionExemptionAdmin)
