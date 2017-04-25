# -*- coding: utf-8 -*-

import json

from django.core import serializers
from django.db import IntegrityError
import stripe

from wikisensei import settings
from .models import Customer, Subscription, SubscriptionEvent

stripe.api_key = settings.STRIPE['secret_key']

def ensure_customer(user):
    assert user.is_authenticated, 'User need to be authenticated.'
    try:
        # If customer exists, get this customer
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        # Create a new customer if not exists
        _customer = stripe.Customer.create(
            id=user.id,
            email=user.email,
        )

        # Bind customer with user.
        customer = Customer(
            user=user,
            stripe_id=_customer.id,
        )
        customer.save()

    return customer

def get_subscription_by_user(user):
    try:
        return Subscription.objects.get(user=user)
    except Subscription.DoesNotExist:
        return

def subscribe(customer, plan, token):
    try:
        subscription = Subscription.objects.get(user=customer.user)
    except Subscription.DoesNotExist:
        subscription = None

    if subscription and subscription.stripe_id:
        # If subscription exists and related to a plan, change it to a new plan.
        _subscription = stripe.Subscription.retrieve(subscription.stripe_id)
        _subscription.plan = plan
        _subscription.source = token
        _subscription.save()

        # log event
        log_subscription_event(customer.user, {
            'action': 'change_subscription',
            'data': {
                'subscription': serializers.serialize('json', [subscription]),
                'raw': str(_subscription)
            }
        })

    else:

        # If subscription does not exists, create a new remote subscription.
        _subscription = stripe.Subscription.create(
            customer=customer.stripe_id,
            plan=plan,
            source=token,
        )
        # Bind stripe id with user.
        subscription = Subscription(
            user=customer.user,
            stripe_id=_subscription.id
        )
        subscription.save()

        # log event
        log_subscription_event(customer.user, {
            'action': 'create_subscription',
            'data': {
                'subscription': serializers.serialize('json', [subscription]),
                'raw': str(_subscription)
            }
        })

    return subscription

def cancel_subscription(subscription):
    if subscription.stripe_id:
        _subscription = stripe.Subscription.retrieve(subscription.stripe_id)
        _subscription.delete()

    log_subscription_event(subscription.user, {
        'action': 'cancel_subscription',
        'data': {
            'subscription': serializers.serialize('json', [subscription]),
        }
    })

    subscription.delete()

def log_subscription_event(user, data):
    event = SubscriptionEvent(
        user=user,
        data=json.dumps(data)
    )
    event.save()

def add_webhook_event(json_data):
    id = json_data['id']
    query = dict(stripe_id=id, data=json.dumps(json_data))
    event, _ = WebhookEvent.objects.get_or_create(**query)
    return event
