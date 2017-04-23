# -*- coding: utf-8 -*-

from .models import Option, CustomStyle

def get_option(user):
    try:
        return user.option
    except Option.DoesNotExist:
        option = Option(user=user)
        option.save()
        return option

def get_custom_style(user):
    try:
        return CustomStyle.objects.get(user=user)
    except (CustomStyle.DoesNotExist, ):
        custom_style = CustomStyle(user=user)
        custom_style.save()
        return custom_style

def is_all_wikis_private(user):
    option = get_option(user)
    return option.private_wiki
