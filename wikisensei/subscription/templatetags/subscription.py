# -*- coding: utf-8 -*-

from collections import Mapping

from django import template
from django.template.loader import get_template

from ..services import get_subscription_by_user

register = template.Library()

def render_template_file(template, context=None):
    """
    Render a Template to unicode
    """
    assert isinstance(context, Mapping)
    template = get_template(template)
    return template.render(context)

@register.simple_tag(takes_context=True)
def cancel_subscription(context, user):
    return render_template_file('subscription/cancel.html', {
        'user': user,
        'context': context,
        'subscription': get_subscription_by_user(user),
    })
