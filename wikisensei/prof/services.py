# -*- coding: utf-8 -*-

from .models import Option

def get_option(user):
    try:
        return user.option
    except Option.DoesNotExist:
        option = Option(user=user)
        option.save()
        return option

def is_all_wikis_private(user):
    option = get_option(user)
    return option.private_wiki
