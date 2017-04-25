# -*- coding: utf-8 -*-

from .models import Subscription
from .services import cancel_subscription

def handle_customer_subscription_deleted(event):
    _subscription = event.data['object']

    try:
        subscription = Subscription.objects.get(stripe_id=_subscription.id)
        cancel_subscription(subscription)
    except Subscription.DoesNotExist:
        # we may have deleted related subscription from database.
        pass

def handle_customer_subscription_trial_will_end(event):
    # XXX: ensure there’s a payment source on the customer so they can be billed
    # XXX: notify the customer that a charge is forthcoming
    pass

def handle_customer_subscription_updated(event):
    # https://stripe.com/docs/api#subscription_object
    # XXX: handle 'pass_due' status: notify user?
    # XXX: handle 'unpaied' status: according to dashboard setting.
    pass

def handle(type, event):
    handler_name = 'handle_%s' % type.replace('.', '_')
    handler = globals().get(handler_name)
    if handler:
        handler(event)
