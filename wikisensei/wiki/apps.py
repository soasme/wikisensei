# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class WikiConfig(AppConfig):
    name = 'wiki'

    def ready(self):
        from .receivers import create_root_wiki
        from allauth.account.signals import user_signed_up
        user_signed_up.connect(create_root_wiki, dispatch_uid='root_wiki_generator')
