# -*- coding: utf-8 -*-

from django import template
import dateutil.parser

register = template.Library()

@register.assignment_tag
def define(val=None):
    return val

@register.filter
def iso8601(value):
    return dateutil.parser.parse(value)
