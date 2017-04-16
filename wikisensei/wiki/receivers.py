# -*- coding: utf-8 -*-

from .services import create_root_wiki as _create_root_wki

def create_root_wiki(sender, **kwargs):
    user = kwargs['user']
    _create_root_wki(user)
