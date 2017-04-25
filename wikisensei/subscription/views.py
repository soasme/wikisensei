# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from wikisensei import settings
from .models import MonthlyPlan, AnnualPlan
from .services import ensure_customer, subscribe, cancel_subscription, get_subscription_by_user
from .webhook import handle as webhook_handler

@login_required
def index(request):
    return render(request, 'subscription/index.html', {
        'key': settings.STRIPE['publishable_key'],
        'monthly_plan': MonthlyPlan(),
        'annual_plan': AnnualPlan(),
    })

@login_required
@require_POST
def charge(request, plan):
    customer = ensure_customer(request.user)
    token = request.POST['stripeToken']
    # FIXME: error handle
    subscription = subscribe(customer, plan, token)
    return redirect('subscribe_successfully')

@login_required
def subscribe_successfully(request):
    return render(request, 'subscription/subscribe.html', {
    })

@login_required
def unsubscribe_successfully(request):
    return render(request, 'subscription/unsubscribe.html', {
    })

@login_required
@require_POST
def unsubscribe(request):
    subscription = get_subscription_by_user(request.user)
    if subscription:
        cancel_subscription(subscription)
        return redirect('unsubscribe_successfully')
    else:
        return redirect('account_profile')

@require_POST
@csrf_exempt
def webhook(request):
    event_json = json.loads(request.body)
    event = stripe.Event.retrieve(event_json["id"])
    add_webhook_event(event_json)
    webhook_handler(event.object, event)
    return HttpResponse(status=200)
